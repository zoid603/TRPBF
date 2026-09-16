from typing import List, Dict, Any, Optional, Generator


def add_achievement(
    achievements: List[Dict[str, Any]],
    game_id: int,
    name: str,
    required_actions: int,
    is_secret: bool = False
) -> Dict[str, Any]:
    """Добавление нового достижения."""
    next_id = max([a["id"] for a in achievements], default=0) + 1
    ach = {
        "id": next_id,
        "game_id": game_id,
        "name": name,
        "required_actions": required_actions,
        "is_secret": is_secret
    }
    achievements.append(ach)
    return ach


def get_achievement_by_id(
    achievements: List[Dict[str, Any]],
    ach_id: int
) -> Optional[Dict[str, Any]]:
    """Поиск ачивки по ID."""
    for ach in achievements:
        if ach["id"] == ach_id:
            return ach
    return None


def find_achievements(
    achievements: List[Dict[str, Any]],
    query: str
) -> Generator[Dict[str, Any], None, None]:
    """Генератор поиска ачивок по подстроке в названии."""
    low_query = query.lower()
    for ach in achievements:
        if low_query in ach["name"].lower():
            yield ach


def sort_achievements_by_complexity(
    achievements: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Сортировка ачивок по сложности через lambda."""
    return sorted(achievements, key=lambda x: x["required_actions"])


def get_achievements_by_game(
    achievements: List[Dict[str, Any]],
    game_id: int
) -> List[Dict[str, Any]]:
    """Получение всех достижений, относящихся к конкретной игре."""
    return [a for a in achievements if a.get("game_id") == game_id]
