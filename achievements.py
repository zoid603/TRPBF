from typing import Generator, Optional

from models import Achievement, Game


def add_achievement(
    achievements: list[Achievement],
    game: Game,
    name: str,
    required_actions: int,
    is_secret: bool = False,
) -> Achievement:
    """Добавить достижение, связанное с объектом игры."""
    next_id = max((item.id for item in achievements), default=0) + 1
    achievement = Achievement(
        id=next_id,
        game=game,
        name=name,
        required_actions=required_actions,
        is_secret=is_secret,
    )
    achievements.append(achievement)
    return achievement


def get_achievement_by_id(
    achievements: list[Achievement],
    achievement_id: int,
) -> Optional[Achievement]:
    """Найти достижение по идентификатору."""
    return next(
        (item for item in achievements if item.id == achievement_id),
        None,
    )


def find_achievements(
    achievements: list[Achievement],
    query: str,
) -> Generator[Achievement, None, None]:
    """Найти достижения по подстроке в названии."""
    normalized = query.casefold()
    yield from (
        item
        for item in achievements
        if normalized in item.name.casefold()
    )


def sort_achievements_by_complexity(
    achievements: list[Achievement],
) -> list[Achievement]:
    """Отсортировать достижения по количеству действий."""
    return sorted(
        achievements,
        key=lambda item: item.required_actions,
    )


def get_achievements_by_game(
    achievements: list[Achievement],
    game: Game,
) -> list[Achievement]:
    """Вернуть достижения выбранной игры."""
    return [item for item in achievements if item.game is game]
