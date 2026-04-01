from fastapi import FastAPI, HTTPException, Response
from app.models import LoginRequest
from app.store import get_user_by_email
from app.routes_users import router as users_router
from app.routes_ops import router as ops_router

app = FastAPI(
    title="User API",
    description="A FastAPI backend for managing users with in-memory storage and HTTP Basic authentication.",
    version="1.0.0",
)

app.include_router(users_router)
app.include_router(ops_router)


@app.head("/")
def health_head():
    return Response(status_code=200)


@app.get("/")
def health_get():
    return {"status": "ok", "service": "user-api"}


@app.post("/login")
def login(body: LoginRequest):
    user = get_user_by_email(body.email)
    if user is None or user.password != body.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}
