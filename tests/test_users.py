import pytest

from models import User
from users import add_user, get_user_by_id, get_user_by_username, show_users


@pytest.mark.smoke
def test_user_creation_and_from_data() -> None:
    users: list[User] = []
    user = add_user(users, "PlayerOne")
    restored = User.from_data({"id": 2, "username": "ProGamer"})

    assert user.id == 1
    assert user.username == "PlayerOne"
    assert str(user) == "ID 1: PlayerOne"
    assert restored.id == 2


@pytest.mark.unit
@pytest.mark.parametrize(
    ("query", "expected"),
    [("playerone", True), ("PLAYERONE", True), ("Unknown", False)],
)
def test_user_search_is_case_insensitive(query: str, expected: bool) -> None:
    user = User(1, "PlayerOne")

    result = get_user_by_username([user], query)

    assert (result is user) is expected


@pytest.mark.unit
def test_user_search_by_id() -> None:
    user = User(7, "PlayerOne")

    assert get_user_by_id([user], 7) is user
    assert get_user_by_id([user], 999) is None


def test_show_users(capsys) -> None:
    show_users([User(1, "PlayerOne"), User(2, "PlayerTwo")])

    output = capsys.readouterr().out

    assert "ID 1: PlayerOne" in output
    assert "ID 2: PlayerTwo" in output
