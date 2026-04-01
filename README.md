# User API

A FastAPI backend for managing users with in-memory storage and HTTP Basic authentication.

## Quick Start

### Local

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Docker Compose

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## API Documentation

- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- See [REST_API.md](REST_API.md) for full endpoint reference.

## Default User

The API comes with a pre-seeded admin user:

- **Email:** admin@example.com
- **Password:** admin123

## Authentication

Protected endpoints use HTTP Basic authentication. Supply any valid user's email and password.
`POST /login` returns HTTP 422 when either `email` or `password` is omitted from the request body.

## Operations

Production-safe endpoints are available at `/healthz`, `/readyz`, and `/version`.
`GET /readyz` returns readiness plus process uptime in seconds.

```bash
curl http://localhost:8000/healthz
```

## License

[MIT](LICENSE.md)
