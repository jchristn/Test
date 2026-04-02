"""Tests for unauthenticated health endpoints."""


def test_head_health(client):
    resp = client.head("/")
    assert resp.status_code == 200


def test_get_health(client):
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "user-api"
