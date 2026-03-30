# REST API Reference

Base URL: `http://localhost:8000`

## Unauthenticated Endpoints

### Health Check (HEAD)

```
HEAD /
```

Returns `200 OK` with no body.

### Health Check (GET)

```
GET /
```

Response `200 OK`:
```json
{"status": "ok", "service": "user-api"}
```

### Login

```
POST /login
Content-Type: application/json
```

Request body:
```json
{"email": "admin@example.com", "password": "admin123"}
```

Response `200 OK`:
```json
{"message": "Login successful"}
```

Response `401 Unauthorized`:
```json
{"detail": "Invalid credentials"}
```

## Authenticated Endpoints

All endpoints below require HTTP Basic authentication using a valid user's email and password.

### List Users

```
GET /users
Authorization: Basic <base64(email:password)>
```

Response `200 OK`:
```json
[{"id": 1, "email": "admin@example.com", "name": "Admin"}]
```

### Get User

```
GET /users/{id}
Authorization: Basic <base64(email:password)>
```

Response `200 OK`:
```json
{"id": 1, "email": "admin@example.com", "name": "Admin"}
```

Response `404 Not Found`:
```json
{"detail": "User not found"}
```

### Create User

```
PUT /users
Authorization: Basic <base64(email:password)>
Content-Type: application/json
```

Request body:
```json
{"email": "user@example.com", "password": "pass123", "name": "New User"}
```

Response `201 Created`:
```json
{"id": 2, "email": "user@example.com", "name": "New User"}
```

Response `409 Conflict`:
```json
{"detail": "Email already in use"}
```

### Update User

```
PUT /users/{id}
Authorization: Basic <base64(email:password)>
Content-Type: application/json
```

Request body (all fields optional):
```json
{"name": "Updated Name"}
```

Response `200 OK`:
```json
{"id": 1, "email": "admin@example.com", "name": "Updated Name"}
```

Response `404 Not Found`:
```json
{"detail": "User not found"}
```

### Check User Exists

```
HEAD /users/{id}
Authorization: Basic <base64(email:password)>
```

Response `200 OK` (no body) or `404 Not Found`.

### Delete User

```
DELETE /users/{id}
Authorization: Basic <base64(email:password)>
```

Response `204 No Content` or `404 Not Found`.
