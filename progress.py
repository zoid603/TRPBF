from datetime import date
from typing import Optional

from models import Achievement, Progress, User


def record_progress(
    progress_list: list[Progress],
    user: User,
    achievement: Achievement,
    completed_actions: int,
    record_date: date | str,
) -> Progress:
    """Добавить или обновить объект прогресса."""
    existing = get_user_progress(progress_list, user, achievement)
    if existing is not None:
        existing.update(completed_actions, str(record_date))
        return existing

    next_id = max((item.id for item in progress_list), default=0) + 1
    progress = Progress(
        id=next_id,
        user=user,
        achievement=achievement,
        completed_actions=completed_actions,
        record_date=str(record_date),
    )
    progress_list.append(progress)
    return progress


def get_user_progress(
    progress_list: list[Progress],
    user: User,
    achievement: Achievement,
) -> Optional[Progress]:
    """Найти прогресс пользователя по достижению."""
    return next(
        (
            item
            for item in progress_list
            if item.user is user and item.achievement is achievement
        ),
        None,
    )


def format_achievement_summary(progress: Progress) -> str:
    """Сформировать карточку прогресса из объекта Progress."""
    return (
        f"--- Карточка игрока: {progress.user.username} ---\n"
        f"Игра: {progress.achievement.game.title}\n"
        f"Достижение: {progress.achievement.name}\n"
        f"Прогресс: {progress.percent()}%\n"
        f"Статус: {progress.status()}\n"
        f"Дата фиксации: {progress.record_date}"
    )
