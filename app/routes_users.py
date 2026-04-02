from fastapi import APIRouter, Depends, HTTPException, Response, status
from app.auth import get_current_user
from app.models import User, UserCreate, UserUpdate, UserResponse
from app import store

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", response_model=list[UserResponse])
def get_users(current_user: User = Depends(get_current_user)):
    return store.list_users()


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    user = store.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, current_user: User = Depends(get_current_user)):
    existing = store.get_user_by_email(body.email)
    if existing is not None:
        raise HTTPException(status_code=409, detail="Email already in use")
    user = store.create_user(email=body.email, password=body.password, name=body.name)
    return user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, body: UserUpdate, current_user: User = Depends(get_current_user)):
    user = store.update_user(user_id, email=body.email, password=body.password, name=body.name)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.head("/{user_id}")
def user_exists(user_id: int, current_user: User = Depends(get_current_user)):
    user = store.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=200)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, current_user: User = Depends(get_current_user)):
    deleted = store.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")
    return Response(status_code=204)
