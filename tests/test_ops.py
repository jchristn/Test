"""Tests for documented ops endpoints."""


def test_healthz_returns_ok(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "name": "user-api"}


def test_healthz_returns_same_service_name_as_version(client):
    healthz_resp = client.get("/healthz")
    version_resp = client.get("/version")

    assert healthz_resp.status_code == 200
    assert version_resp.status_code == 200
    assert healthz_resp.json()["name"] == version_resp.json()["name"] == "user-api"


def test_version_returns_service_metadata(client):
    resp = client.get("/version")
    assert resp.status_code == 200
    assert resp.json() == {"version": "1.0.0", "name": "user-api", "status": "stable"}
