"""Tests for the GET /readyz readiness endpoint."""

from unittest.mock import patch


def test_readyz_returns_ready(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


def test_readyz_returns_same_service_identity_as_healthz(client):
    readyz_resp = client.get("/readyz")
    healthz_resp = client.get("/healthz")

    assert readyz_resp.status_code == 200
    assert healthz_resp.status_code == 200
    assert readyz_resp.json()["name"] == healthz_resp.json()["name"] == "user-api"
    assert readyz_resp.json()["version"] == healthz_resp.json()["version"] == "1.0.0"


def test_readyz_returns_503_when_store_unavailable(client):
    with patch("app.routes_ops.list_users", side_effect=RuntimeError("store down")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    assert resp.json() == {"status": "not_ready", "reason": "store down"}


def test_readyz_returns_503_on_generic_exception(client):
    with patch("app.routes_ops.list_users", side_effect=Exception("unexpected")):
        resp = client.get("/readyz")
    assert resp.status_code == 503
    data = resp.json()
    assert data["status"] == "not_ready"
    assert "unexpected" in data["reason"]
