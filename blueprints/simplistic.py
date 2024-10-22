import logging
import random

from flask import Blueprint, abort, current_app, jsonify, request
from prometheus_client import Counter, Histogram, generate_latest

from models import RequestLog
from services import get_random
from utils import get_now_time

# Define the blueprint
simplistic_bp = Blueprint("simplistic", __name__)

# Set up logging
logger = logging.getLogger("app_logger")

# Prometheus metrics
REQUEST_COUNT = Counter("request_count", "Total Request Count", ["endpoint", "method"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency", ["endpoint"])


@simplistic_bp.route("/data", methods=["GET", "POST"])
def data() -> None:
    """Data endpoint returning a wrapped response from a downstream"""
    logger.debug(f"Received {request.method} request on /data")
    if request.method == "GET":
        try:
            return jsonify(
                {
                    "remote_random_data": get_random(
                        remote_url=current_app.config.get("REMOTE_RANDOM_URL")
                    )
                }
            )
        except (TypeError, ValueError, Exception) as error:
            logger.error(f"Downstream call failed with error: {error}")
            abort(503)
    elif request.method == "POST":
        return jsonify(request.get_json())


@simplistic_bp.route("/error", methods=["GET"])
def error() -> None:
    """Return a random HTTP error"""
    errors = [400, 401, 404, 419, 429, 500, 503]
    return "", random.choice(errors)


@simplistic_bp.route("/metrics", methods=["GET"])
def metrics() -> None:
    """Emit prometheus metrics for being scrapped"""
    return generate_latest(), 200


@simplistic_bp.before_request
def start_timer() -> None:
    """Set the start time of a request"""
    request.start_time = get_now_time()


@simplistic_bp.after_request
def log_request(response) -> None:
    """Write the request details into the database"""
    latency = (get_now_time() - request.start_time).total_seconds()
    REQUEST_LATENCY.labels(request.endpoint).observe(latency)
    REQUEST_COUNT.labels(request.endpoint, request.method).inc()

    # Log the request
    log_data = RequestLog(
        ip_address=request.remote_addr,
        endpoint=request.path,
        method=request.method,
        response_code=response.status_code,
        timestamp=get_now_time(),
    )
    current_app.db.session.add(log_data)
    current_app.db.session.commit()

    return response
