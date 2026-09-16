from typing import List, Dict, Any, Optional


def add_game(games: List[Dict[str, Any]], title: str) -> Dict[str, Any]:
    """Добавление новой игры в систему."""
    next_id = max([g["id"] for g in games], default=0) + 1
    new_game = {"id": next_id, "title": title}
    games.append(new_game)
    return new_game


def get_game_by_id(
    games: List[Dict[str, Any]],
    game_id: int
) -> Optional[Dict[str, Any]]:
    """Поиск игры по ID."""
    for game in games:
        if game["id"] == game_id:
            return game
    return None
