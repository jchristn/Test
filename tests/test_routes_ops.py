import pytest
from unittest.mock import patch
from flask import Flask

from app.routes_ops import ops_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(ops_bp)
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthz:
    def test_healthz_returns_200(self, client):
        resp = client.get("/healthz")
        assert resp.status_code == 200

    def test_healthz_contains_name_and_version(self, client):
        data = client.get("/healthz").get_json()
        assert data["status"] == "healthy"
        assert data["name"] == "user-api"
        assert data["version"] == "1.0.0"


class TestVersion:
    def test_version_returns_200(self, client):
        resp = client.get("/version")
        assert resp.status_code == 200

    def test_version_contains_name_and_version(self, client):
        data = client.get("/version").get_json()
        assert data["name"] == "user-api"
        assert data["version"] == "1.0.0"


class TestReadyz:
    def test_readyz_returns_200(self, client):
        resp = client.get("/readyz")
        assert resp.status_code == 200

    def test_readyz_success_contains_status(self, client):
        data = client.get("/readyz").get_json()
        assert data["status"] == "ready"

    def test_readyz_success_contains_name(self, client):
        data = client.get("/readyz").get_json()
        assert data["name"] == "user-api"

    def test_readyz_success_contains_version(self, client):
        data = client.get("/readyz").get_json()
        assert data["version"] == "1.0.0"

    def test_readyz_success_contains_uptime_seconds(self, client):
        data = client.get("/readyz").get_json()
        assert "uptime_seconds" in data
        assert isinstance(data["uptime_seconds"], float)

    def test_readyz_success_has_all_expected_keys(self, client):
        data = client.get("/readyz").get_json()
        assert set(data.keys()) == {"status", "name", "version", "uptime_seconds"}

    def test_readyz_error_returns_503(self, client):
        with patch("app.routes_ops.time") as mock_time:
            mock_time.time.side_effect = [RuntimeError("clock failure")]
            resp = client.get("/readyz")
            assert resp.status_code == 503

    def test_readyz_error_contains_name_and_version(self, client):
        with patch("app.routes_ops.time") as mock_time:
            mock_time.time.side_effect = [RuntimeError("clock failure")]
            data = client.get("/readyz").get_json()
            assert data["status"] == "not_ready"
            assert data["name"] == "user-api"
            assert data["version"] == "1.0.0"
            assert data["reason"] == "clock failure"

    def test_readyz_error_has_all_expected_keys(self, client):
        with patch("app.routes_ops.time") as mock_time:
            mock_time.time.side_effect = [RuntimeError("boom")]
            data = client.get("/readyz").get_json()
            assert set(data.keys()) == {"status", "name", "version", "reason"}
