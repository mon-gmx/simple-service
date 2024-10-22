class Config:
    DEBUG = False
    TESTING = False
    REMOTE_RANDOM_URL = "http://localhost/data"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://user:password@database-server/simpleservice"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    USE_OTEL = False
    JAEGER_SETTINGS = {}
    HONEYCOMB_SETTINGS = {}


class DevelopmentConfig(Config):
    DEBUG = True
    USE_OTEL = True
    JAEGER_SETTINGS = {
        "USE_JAEGER": True,
        "host": "jaeger-server",
        "port": 6831,
    }
    HONEYCOMB_SETTINGS = {
        "USE_HONEYCOMB": True,
        "HONEYCOMB_API": "https://api.honeycomb.io:443",
        "HONEYCOMB_DATASET": "simple-service",
        "HONEYCOMB_API_KEY": "00000000000000000000",
    }
    REMOTE_RANDOM_URL = "http://remote-service-fqdn/data"


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    USE_OTEL = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use SQLite for tests
    SQLALCHEMY_TRACK_MODIFICATIONS = False
