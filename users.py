from typing import Optional

from models import User


def add_user(users: list[User], username: str) -> User:
    """Добавить пользователя с новым идентификатором."""
    next_id = max((user.id for user in users), default=0) + 1
    user = User(id=next_id, username=username)
    users.append(user)
    return user


def get_user_by_username(
    users: list[User],
    username: str,
) -> Optional[User]:
    """Найти пользователя по имени без учета регистра."""
    normalized = username.casefold()
    return next(
        (user for user in users if user.username.casefold() == normalized),
        None,
    )


def get_user_by_id(users: list[User], user_id: int) -> Optional[User]:
    """Найти пользователя по идентификатору."""
    return next((user for user in users if user.id == user_id), None)


def show_users(users: list[User]) -> None:
    """Вывести список всех игроков."""
    print("\n--- Список игроков ---")
    if not users:
        print("Игроки еще не добавлены.")
        return
    for user in users:
        print(user)
