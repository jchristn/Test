"""Tests for documented ops endpoints."""


def test_healthz_returns_ok(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_version_returns_service_metadata(client):
    resp = client.get("/version")
    assert resp.status_code == 200
    assert resp.json() == {"version": "1.0.0", "name": "user-api"}
