from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from app.store import get_user_by_email
from app.models import User

security = HTTPBasic()


def get_current_user(credentials: HTTPBasicCredentials = Depends(security)) -> User:
    user = get_user_by_email(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return user
