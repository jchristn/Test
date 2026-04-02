"""Tests for documented ops endpoints."""


def test_healthz_returns_ok(client):
    resp = client.get("/healthz")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "name": "user-api", "version": "1.0.0"}


def test_ops_endpoints_return_consistent_service_identity(client):
    readyz_resp = client.get("/readyz")
    healthz_resp = client.get("/healthz")
    version_resp = client.get("/version")

    assert readyz_resp.status_code == 200
    assert healthz_resp.status_code == 200
    assert version_resp.status_code == 200
    assert readyz_resp.json()["name"] == healthz_resp.json()["name"] == version_resp.json()["name"] == "user-api"
    assert readyz_resp.json()["version"] == healthz_resp.json()["version"] == version_resp.json()["version"] == "1.0.0"


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
