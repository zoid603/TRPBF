from typing import Optional

from models import Game


def add_game(games: list[Game], title: str) -> Game:
    """Добавить игру с новым идентификатором."""
    next_id = max((game.id for game in games), default=0) + 1
    game = Game(id=next_id, title=title)
    games.append(game)
    return game


def get_game_by_id(
    games: list[Game],
    game_id: int,
) -> Optional[Game]:
    """Найти игру по идентификатору."""
    return next((game for game in games if game.id == game_id), None)
