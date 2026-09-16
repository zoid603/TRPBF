from typing import List, Dict, Any, Optional


def add_user(users: List[Dict[str, Any]], username: str) -> Dict[str, Any]:
    """Добавление пользователя с автоинкрементом ID."""
    next_id = max([u["id"] for u in users], default=0) + 1
    new_user = {"id": next_id, "username": username}
    users.append(new_user)
    return new_user


def get_user_by_username(
    users: List[Dict[str, Any]],
    username: str
) -> Optional[Dict[str, Any]]:
    """Поиск пользователя по имени."""
    for user in users:
        if user["username"].lower() == username.lower():
            return user
    return None
