"""Tests for the GET /readyz readiness endpoint."""

import time

from unittest.mock import patch


def test_readyz_returns_ready(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


def test_readyz_response_contains_name(client):
    """Verify readyz includes the service name per REST_API.md docs."""
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "user-api"


def test_readyz_response_contains_version(client):
    """Verify readyz includes the service version per REST_API.md docs."""
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["version"] == "1.0.0"


def test_readyz_response_has_all_documented_fields(client):
    """Verify readyz response contains all fields documented in REST_API.md."""
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    expected_keys = {"status", "name", "version", "uptime_seconds"}
    assert set(data.keys()) == expected_keys


def test_readyz_returns_json_content_type(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    assert resp.headers["content-type"] == "application/json"


def test_readyz_uptime_increases_over_time(client):
    resp1 = client.get("/readyz")
    time.sleep(0.05)
    resp2 = client.get("/readyz")
    assert resp2.json()["uptime_seconds"] >= resp1.json()["uptime_seconds"]


def test_readyz_returns_503_when_store_unavailable(client):
    with patch("app.routes_ops.list_users", side_effect=RuntimeError("store down")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "not_ready"
    assert "store down" in data["reason"]


def test_readyz_503_does_not_contain_uptime(client):
    """When not ready, uptime_seconds should not be in the response."""
    with patch("app.routes_ops.list_users", side_effect=RuntimeError("store down")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert "uptime_seconds" not in data


def test_readyz_returns_503_on_generic_exception(client):
    with patch("app.routes_ops.list_users", side_effect=Exception("unexpected")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "not_ready"
    assert "unexpected" in data["reason"]
