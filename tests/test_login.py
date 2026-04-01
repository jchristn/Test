"""Tests for the POST /login endpoint."""


def test_login_success(client):
    resp = client.post("/login", json={"email": "admin@example.com", "password": "admin123"})
    assert resp.status_code == 200
    assert resp.json()["message"] == "Login successful"


def test_login_wrong_password(client):
    resp = client.post("/login", json={"email": "admin@example.com", "password": "wrong"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "Invalid credentials"


def test_login_unknown_email(client):
    resp = client.post("/login", json={"email": "nobody@example.com", "password": "x"})
    assert resp.status_code == 401


def test_login_missing_password(client):
    resp = client.post("/login", json={"email": "admin@example.com"})
    assert resp.status_code == 422


def test_login_missing_email(client):
    resp = client.post("/login", json={"password": "admin123"})
    assert resp.status_code == 422
