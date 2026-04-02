from typing import Optional
from app.models import User

_next_id = 2

_users: dict[int, User] = {
    1: User(id=1, email="admin@example.com", password="admin123", name="Admin"),
}


def get_user_by_email(email: str) -> Optional[User]:
    for user in _users.values():
        if user.email == email:
            return user
    return None


def get_user_by_id(user_id: int) -> Optional[User]:
    return _users.get(user_id)


def list_users() -> list[User]:
    return list(_users.values())


def create_user(email: str, password: str, name: str) -> User:
    global _next_id
    user = User(id=_next_id, email=email, password=password, name=name)
    _users[_next_id] = user
    _next_id += 1
    return user


def update_user(user_id: int, email: Optional[str] = None, password: Optional[str] = None, name: Optional[str] = None) -> Optional[User]:
    user = _users.get(user_id)
    if user is None:
        return None
    if email is not None:
        user.email = email
    if password is not None:
        user.password = password
    if name is not None:
        user.name = name
    _users[user_id] = user
    return user


def delete_user(user_id: int) -> bool:
    if user_id in _users:
        del _users[user_id]
        return True
    return False
