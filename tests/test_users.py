"""Tests for authenticated /users endpoints."""


# --- Authentication ---

def test_users_requires_auth(client):
    resp = client.get("/users")
    assert resp.status_code == 401


def test_users_bad_credentials(client):
    resp = client.get("/users", auth=("admin@example.com", "wrong"))
    assert resp.status_code == 401


# --- GET /users ---

def test_list_users(client, auth):
    resp = client.get("/users", auth=auth)
    assert resp.status_code == 200
    users = resp.json()
    assert len(users) == 1
    assert users[0]["email"] == "admin@example.com"
    assert "password" not in users[0]


# --- GET /users/{id} ---

def test_get_user_by_id(client, auth):
    resp = client.get("/users/1", auth=auth)
    assert resp.status_code == 200
    assert resp.json()["id"] == 1
    assert resp.json()["name"] == "Admin"
    assert "password" not in resp.json()


def test_get_user_not_found(client, auth):
    resp = client.get("/users/999", auth=auth)
    assert resp.status_code == 404


# --- PUT /users (create) ---

def test_create_user(client, auth):
    resp = client.put(
        "/users",
        json={"email": "new@example.com", "password": "pass1", "name": "New"},
        auth=auth,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "new@example.com"
    assert data["name"] == "New"
    assert "password" not in data
    assert data["id"] == 2


def test_create_user_duplicate_email(client, auth):
    resp = client.put(
        "/users",
        json={"email": "admin@example.com", "password": "x", "name": "Dup"},
        auth=auth,
    )
    assert resp.status_code == 409
    assert resp.json()["detail"] == "Email already in use"


def test_create_user_missing_fields(client, auth):
    resp = client.put("/users", json={"email": "x@x.com"}, auth=auth)
    assert resp.status_code == 422


# --- PUT /users/{id} (update) ---

def test_update_user_name(client, auth):
    resp = client.put("/users/1", json={"name": "Updated"}, auth=auth)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Updated"


def test_update_user_email(client, auth):
    resp = client.put("/users/1", json={"email": "new@admin.com"}, auth=auth)
    assert resp.status_code == 200
    assert resp.json()["email"] == "new@admin.com"


def test_update_user_not_found(client, auth):
    resp = client.put("/users/999", json={"name": "X"}, auth=auth)
    assert resp.status_code == 404


# --- HEAD /users/{id} ---

def test_user_exists(client, auth):
    resp = client.head("/users/1", auth=auth)
    assert resp.status_code == 200


def test_user_exists_not_found(client, auth):
    resp = client.head("/users/999", auth=auth)
    assert resp.status_code == 404


def test_user_exists_requires_auth(client):
    resp = client.head("/users/1")
    assert resp.status_code == 401


# --- DELETE /users/{id} ---

def test_delete_user(client, auth):
    # Create a user to delete
    client.put(
        "/users",
        json={"email": "del@example.com", "password": "p", "name": "Del"},
        auth=auth,
    )
    resp = client.delete("/users/2", auth=auth)
    assert resp.status_code == 204

    # Verify deleted
    resp = client.get("/users/2", auth=auth)
    assert resp.status_code == 404


def test_delete_user_not_found(client, auth):
    resp = client.delete("/users/999", auth=auth)
    assert resp.status_code == 404


def test_delete_requires_auth(client):
    resp = client.delete("/users/1")
    assert resp.status_code == 401


# --- Integration: create then authenticate as new user ---

def test_new_user_can_authenticate(client, auth):
    client.put(
        "/users",
        json={"email": "u2@example.com", "password": "secret", "name": "U2"},
        auth=auth,
    )
    resp = client.get("/users", auth=("u2@example.com", "secret"))
    assert resp.status_code == 200
    assert len(resp.json()) == 2


# --- OpenAPI docs ---

def test_openapi_docs(client):
    resp = client.get("/docs")
    assert resp.status_code == 200

    resp = client.get("/openapi.json")
    assert resp.status_code == 200
    schema = resp.json()
    assert schema["info"]["title"] == "User API"
