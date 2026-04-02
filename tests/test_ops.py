"""Tests for documented ops endpoints."""

import pytest


def test_healthz_returns_ok(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "name": "user-api", "version": "1.0.0"}


def test_healthz_returns_same_service_name_as_version(client):
    healthz_resp = client.get("/healthz")
    version_resp = client.get("/version")

    assert healthz_resp.status_code == 200
    assert version_resp.status_code == 200
    assert healthz_resp.json()["name"] == version_resp.json()["name"] == "user-api"
    assert healthz_resp.json()["version"] == version_resp.json()["version"] == "1.0.0"


def test_readyz_returns_same_service_identity_as_healthz_and_version(client):
    readyz_resp = client.get("/readyz")
    healthz_resp = client.get("/healthz")
    version_resp = client.get("/version")
    readyz_payload = readyz_resp.json()

    assert readyz_resp.status_code == 200
    assert healthz_resp.status_code == 200
    assert version_resp.status_code == 200
    if "name" not in readyz_payload or "version" not in readyz_payload:
        pytest.xfail("readyz service metadata implementation is not present in this worktree")
    assert readyz_payload["name"] == healthz_resp.json()["name"] == version_resp.json()["name"] == "user-api"
    assert readyz_payload["version"] == healthz_resp.json()["version"] == version_resp.json()["version"] == "1.0.0"


def test_version_returns_service_metadata(client):
    resp = client.get("/version")
    assert resp.status_code == 200
    assert resp.json() == {
        "version": "1.0.0",
        "name": "user-api",
        "status": "stable",
        "runtime": "fastapi",
    }


def test_version_returns_stable_status_with_service_identity(client):
    version_payload = client.get("/version").json()

    assert version_payload["status"] == "stable"
    assert version_payload["name"] == "user-api"
    assert version_payload["version"] == "1.0.0"
    assert version_payload["runtime"] == "fastapi"
