"""Tests for the GET /readyz readiness endpoint."""

from unittest.mock import patch


def test_readyz_returns_ready(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


def test_readyz_returns_503_when_store_unavailable(client):
    with patch("app.routes_ops.list_users", side_effect=RuntimeError("store down")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "not_ready"
    assert "store down" in data["reason"]
    assert "store down" in data["detail"]


def test_readyz_returns_503_on_generic_exception(client):
    with patch("app.routes_ops.list_users", side_effect=Exception("unexpected")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "not_ready"
    assert "unexpected" in data["reason"]
