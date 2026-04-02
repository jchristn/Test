"""Tests for the GET /readyz readiness endpoint."""

from unittest.mock import patch


def test_readyz_returns_ready(client):
    with patch("app.routes_ops.list_users") as mock_list_users, patch(
        "app.routes_ops.PROCESS_START_TIME", 100.0
    ), patch("app.routes_ops.time.monotonic", return_value=123.5):
        resp = client.get("/readyz")

    assert resp.status_code == 200
    assert resp.json() == {
        "status": "ready",
        "name": "user-api",
        "version": "1.0.0",
        "uptime_seconds": 23.5,
    }
    mock_list_users.assert_called_once_with()


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
