import pytest
from games import add_game, get_game_by_id


@pytest.mark.smoke
def test_add_game_success():
    """1. Проверка успешного добавления игры."""
    games = []
    game = add_game(games, "DOOM")
    assert len(games) == 1
    assert game["id"] == 1
    assert game["title"] == "DOOM"


@pytest.mark.unit
def test_add_game_incremental_id():
    """2. Проверка автоинкремента ID при добавлении нескольких игр."""
    games = []
    g1 = add_game(games, "DOOM")
    g2 = add_game(games, "Witcher 3")
    assert g1["id"] == 1
    assert g2["id"] == 2
    assert len(games) == 2


@pytest.mark.unit
@pytest.mark.parametrize(
    "target_id, expected_title",
    [
        (1, "DOOM"),
        (2, "Cyberpunk 2077"),
    ],
)
def test_get_game_by_id_found(target_id: int, expected_title: str):
    """3. Параметризованный поиск игры по первичному ключу ID."""
    games = [
        {"id": 1, "title": "DOOM"},
        {"id": 2, "title": "Cyberpunk 2077"},
    ]
    game = get_game_by_id(games, target_id)
    assert game is not None
    assert game["title"] == expected_title


@pytest.mark.unit
@pytest.mark.parametrize("missing_id", [0, -1, 999])
def test_get_game_by_id_not_found(missing_id: int):
    """4. Параметризованный поиск по отсутствующему ID."""
    games = [{"id": 1, "title": "DOOM"}]
    assert get_game_by_id(games, missing_id) is None
