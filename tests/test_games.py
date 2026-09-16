from games import add_game, get_game_by_id
from models import Game


def test_game_creation_and_string() -> None:
    games: list[Game] = []
    game = add_game(games, "DOOM")

    assert game.id == 1
    assert game.title == "DOOM"
    assert str(game) == "ID 1: DOOM"


def test_game_search_returns_same_object() -> None:
    games = [Game(1, "DOOM")]

    assert get_game_by_id(games, 1) is games[0]
    assert get_game_by_id(games, 999) is None
