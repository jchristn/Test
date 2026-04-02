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


def test_readyz_returns_same_service_identity_as_healthz_and_version(client):
    readyz_resp = client.get("/readyz")
    healthz_resp = client.get("/healthz")
    version_resp = client.get("/version")

    assert readyz_resp.status_code == 200
    assert healthz_resp.status_code == 200
    assert version_resp.status_code == 200
    assert readyz_resp.json()["name"] == healthz_resp.json()["name"] == version_resp.json()["name"] == "user-api"
    assert readyz_resp.json()["version"] == healthz_resp.json()["version"] == version_resp.json()["version"] == "1.0.0"


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
