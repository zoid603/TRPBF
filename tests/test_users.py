from models import User
from users import add_user, get_user_by_username


def test_user_creation_and_from_data() -> None:
    users: list[User] = []
    user = add_user(users, "PlayerOne")
    restored = User.from_data({"id": 2, "username": "ProGamer"})

    assert user.id == 1
    assert user.username == "PlayerOne"
    assert str(user) == "ID 1: PlayerOne"
    assert restored.id == 2


def test_user_search_is_case_insensitive() -> None:
    user = User(1, "PlayerOne")

    assert get_user_by_username([user], "playerone") is user
    assert get_user_by_username([user], "Unknown") is None
