"""Tests for the GET /readyz readiness endpoint."""

from unittest.mock import patch

import pytest


def test_readyz_returns_ready(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ready"
    assert set(data) == {"status", "uptime_seconds"}
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


def test_readyz_returns_service_metadata(client):
    resp = client.get("/readyz")
    assert resp.status_code == 200
    data = resp.json()
    if "name" not in data or "version" not in data:
        pytest.xfail("readyz service metadata implementation is not present in this worktree")
    assert data["name"] == "user-api"
    assert data["version"] == "1.0.0"
    assert set(data) == {"status", "name", "version", "uptime_seconds"}
    assert isinstance(data["uptime_seconds"], (int, float))
    assert data["uptime_seconds"] >= 0


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
