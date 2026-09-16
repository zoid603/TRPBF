from datetime import date
from typing import List, Dict, Any, Optional


def calculate_progress_percent(completed: int, total: int) -> float:
    """Расчет процента завершения (из ПР1)."""
    if total <= 0:
        return 0.0
    percent = (completed / total) * 100.0
    if percent > 100.0:
        return 100.0
    return round(percent, 2)


def check_unlock_status(completed: int, total: int) -> str:
    """Определение статуса разблокировки (из ПР1)."""
    if completed >= total and total > 0:
        return "Получено"
    elif completed > 0:
        return "В процессе"
    return "Не начато"


def format_achievement_summary(
    username: str,
    game: str,
    ach_name: str,
    status: str,
    progress: float,
    unlock_day: str
) -> str:
    """Форматирование карточки игрока (из ПР1)."""
    return (
        f"--- Карточка игрока: {username} ---\n"
        f"Игра: {game}\n"
        f"Достижение: {ach_name}\n"
        f"Прогресс: {progress}%\n"
        f"Статус: {status}\n"
        f"Дата фиксации: {unlock_day}"
    )


def record_progress(
    progress_list: List[Dict[str, Any]],
    user_id: int,
    achievement_id: int,
    completed_actions: int,
    record_date: date
) -> Dict[str, Any]:
    """Добавление или обновление прогресса."""
    for item in progress_list:
        if (item["achievement_id"] == achievement_id and
                item["user_id"] == user_id):
            item["completed_actions"] = completed_actions
            item["record_date"] = str(record_date)
            return item

    next_id = max([p["id"] for p in progress_list], default=0) + 1
    new_record = {
        "id": next_id,
        "user_id": user_id,
        "achievement_id": achievement_id,
        "completed_actions": completed_actions,
        "record_date": str(record_date)
    }
    progress_list.append(new_record)
    return new_record


def get_user_progress(
    progress_list: List[Dict[str, Any]],
    user_id: int,
    achievement_id: int
) -> Optional[Dict[str, Any]]:
    """Поиск прогресса конкретного игрока."""
    for item in progress_list:
        if (item["achievement_id"] == achievement_id and
                item["user_id"] == user_id):
            return item
    return None
