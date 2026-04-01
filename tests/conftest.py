import pytest
from fastapi.testclient import TestClient
from app import store
from app.models import User


@pytest.fixture(autouse=True)
def reset_store():
    """Reset the in-memory store before each test."""
    store._users.clear()
    store._next_id = 2
    store._users[1] = User(id=1, email="admin@example.com", password="admin123", name="Admin")
    yield
    store._users.clear()


@pytest.fixture
def client():
    from app.main import app
    return TestClient(app)


@pytest.fixture
def auth():
    """Return basic auth tuple for the default admin user."""
    return ("admin@example.com", "admin123")
