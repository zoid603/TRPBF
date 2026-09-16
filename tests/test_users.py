import pytest
from users import add_user, get_user_by_username


@pytest.mark.smoke
def test_add_user_success():
    """1. Проверка успешного добавления нового пользователя."""
    users = []
    user = add_user(users, "PlayerOne")
    assert len(users) == 1
    assert user["id"] == 1
    assert user["username"] == "PlayerOne"


@pytest.mark.unit
def test_add_multiple_users_auto_id():
    """2. Проверка корректной генерации автоинкрементного ID."""
    users = []
    u1 = add_user(users, "FirstPlayer")
    u2 = add_user(users, "SecondPlayer")
    assert u1["id"] == 1
    assert u2["id"] == 2
    assert len(users) == 2


@pytest.mark.unit
@pytest.mark.parametrize(
    "query, expected_id",
    [
        ("Gamer2026", 1),
        ("gamer2026", 1),
        ("GAMER2026", 1),
    ],
)
def test_get_user_by_username_case_insensitive(query: str, expected_id: int):
    """3. Параметризованный поиск пользователя независимо от регистра."""
    users = [{"id": 1, "username": "Gamer2026"}]
    found = get_user_by_username(users, query)
    assert found is not None
    assert found["id"] == expected_id


@pytest.mark.unit
@pytest.mark.parametrize(
    "query",
    ["NonExistent", "Admin", ""],
)
def test_get_user_by_username_not_found(query: str):
    """4. Параметризованная проверка отсутствующих пользователей."""
    users = [{"id": 1, "username": "PlayerOne"}]
    assert get_user_by_username(users, query) is None
