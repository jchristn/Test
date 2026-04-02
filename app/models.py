from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    email: str
    password: str
    name: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None


class UserResponse(BaseModel):
    id: int
    email: str
    name: str


class LoginRequest(BaseModel):
    email: str
    password: str
