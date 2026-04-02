"""Tests for the GET /readyz readiness endpoint."""

from unittest.mock import patch


def test_readyz_returns_ready(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert data["name"] == "user-api"
    assert data["version"] == "1.0.0"
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


def test_readyz_response_contains_exact_keys(client):
    """Verify the success response schema has exactly the expected fields."""
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert set(data.keys()) == {"status", "name", "version", "uptime_seconds"}


def test_readyz_name_and_version_are_strings(client):
    """Verify name and version are non-empty strings."""
    resp = client.get("/readyz")
    data = resp.json()
    assert isinstance(data["name"], str) and len(data["name"]) > 0
    assert isinstance(data["version"], str) and len(data["version"]) > 0


def test_readyz_uptime_increases_between_calls(client):
    """Verify uptime_seconds is non-decreasing across sequential requests."""
    resp1 = client.get("/readyz")
    resp2 = client.get("/readyz")
    t1 = resp1.json()["uptime_seconds"]
    t2 = resp2.json()["uptime_seconds"]
    assert t2 >= t1


def test_readyz_error_response_omits_metadata(client):
    """When readyz returns 503, the response should not contain name/version/uptime."""
    with patch("app.routes_ops.list_users", side_effect=RuntimeError("down")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert set(data.keys()) == {"status", "reason"}
    assert "name" not in data
    assert "version" not in data
    assert "uptime_seconds" not in data


def test_readyz_returns_503_when_store_unavailable(client):
    with patch("app.routes_ops.list_users", side_effect=RuntimeError("store down")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "not_ready"
    assert "store down" in data["reason"]


def test_readyz_returns_503_on_generic_exception(client):
    with patch("app.routes_ops.list_users", side_effect=Exception("unexpected")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "not_ready"
    assert "unexpected" in data["reason"]
