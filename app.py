import logging
import logging.config

import yaml
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            SimpleSpanProcessor)
from prometheus_client import CollectorRegistry

from blueprints.simplistic import simplistic_bp
from config import DevelopmentConfig, TestConfig
from models import RequestLog


def create_app(config_class: object = DevelopmentConfig) -> object:
    with open("logging.yaml", "r") as f:
        logging_config = yaml.safe_load(f.read())
        logging.config.dictConfig(logging_config)
    app = Flask(__name__)
    app.db = SQLAlchemy()
    app.config.from_object(config_class)
    registry = CollectorRegistry()

    # Initialize the database
    app.db.init_app(app)

    # Register the blueprint
    app.register_blueprint(simplistic_bp)

    # OTEL tracing

    use_otel = app.config.get("USE_OTEL", False)
    if use_otel:
        with app.app_context():

            resource = Resource.create({"service.name": "simple_service"})
            trace.set_tracer_provider(TracerProvider(resource=resource))

            jaeger_config = app.config.get("JAEGER_SETTINGS", {})

            if jaeger_config.get("USE_JAEGER"):
                jaeger_config = app.config.get("JAEGER_SETTINGS")
                jaeger_exporter = JaegerExporter(
                    agent_host_name=jaeger_config.get("host"),
                    agent_port=jaeger_config.get("port"),
                )
                trace.get_tracer_provider().add_span_processor(
                    SimpleSpanProcessor(jaeger_exporter)
                )

            honeycomb_config = app.config.get("HONEYCOMB_SETTINGS")
            if honeycomb_config.get("USE_HONEYCOMB"):
                honeycomb_exporter = OTLPSpanExporter(
                    endpoint=honeycomb_config.get("HONEYCOMB_API"),
                    headers={
                        "x-honeycomb-team": honeycomb_config.get("HONEYCOMB_API_KEY"),
                        "x-honeycomb-dataset": honeycomb_config.get(
                            "HONEYCOMB_DATASET"
                        ),
                    },
                )
                trace.get_tracer_provider().add_span_processor(
                    BatchSpanProcessor(honeycomb_exporter)
                )

            RequestsInstrumentor().instrument()
            FlaskInstrumentor().instrument_app(app)
            SQLAlchemyInstrumentor().instrument(engine=app.db.engine)
    return app
