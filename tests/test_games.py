import pytest

from games import add_game, get_game_by_id
from models import Game


@pytest.mark.smoke
def test_game_creation_and_string() -> None:
    games: list[Game] = []
    game = add_game(games, "DOOM")

    assert game.id == 1
    assert game.title == "DOOM"
    assert str(game) == "ID 1: DOOM"


@pytest.mark.unit
@pytest.mark.parametrize(
    ("game_id", "expected_index"),
    [(1, 0), (999, None)],
)
def test_game_search_returns_same_object(
    game_id: int,
    expected_index: int | None,
) -> None:
    games = [Game(1, "DOOM")]

    result = get_game_by_id(games, game_id)
    expected = None if expected_index is None else games[expected_index]

    assert result is expected
