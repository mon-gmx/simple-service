import pytest
from app import create_app
from config import TestConfig
from models import Base

@pytest.fixture(scope="session")
def app() -> object:
    """Create and configure a new app instance for each test session."""
    app = create_app(TestConfig)
    return app


@pytest.fixture(scope="session")
def client(app) -> object:
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="function")
def init_db(app) -> None:
    """Set up an SQLite in-memory database for each test."""
    with app.app_context():
        Base.metadata.create_all(app.db.engine)
        yield app.db
        Base.metadata.drop_all(app.db.engine)


@pytest.fixture
def mock_remote_get_random() -> None:
    """Fixture to send a GET request to a downstream"""
    with patch('requests.get') as mock_get:
        yield mock_get
