import json
import os
from typing import Any

from models import Achievement, Game, Progress, User


def _load_records(filepath: str) -> list[dict[str, Any]]:
    """Загрузить список словарей из JSON."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def _save_records(filepath: str, data: list[dict[str, Any]]) -> None:
    """Сохранить список словарей в JSON-файл."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_games(filepath: str) -> list[Game]:
    """Загрузить игры как объекты Game."""
    return [Game(id=int(item["id"]), title=str(item["title"]))
            for item in _load_records(filepath)]


def save_games(filepath: str, games: list[Game]) -> None:
    """Сохранить объекты Game в формате ПР2."""
    _save_records(
        filepath,
        [{"id": game.id, "title": game.title} for game in games],
    )


def load_users(filepath: str) -> list[User]:
    """Загрузить пользователей как объекты User."""
    return [User.from_data(item) for item in _load_records(filepath)]


def save_users(filepath: str, users: list[User]) -> None:
    """Сохранить объекты User в формате ПР2."""
    _save_records(
        filepath,
        [{"id": user.id, "username": user.username} for user in users],
    )


def load_achievements(
    filepath: str,
    games: list[Game],
) -> list[Achievement]:
    """Загрузить достижения и связать их с объектами Game."""
    games_by_id = {game.id: game for game in games}
    achievements = []
    for item in _load_records(filepath):
        game = games_by_id.get(int(item["game_id"]))
        if game is None:
            continue
        achievements.append(
            Achievement(
                id=int(item["id"]),
                game=game,
                name=str(item["name"]),
                required_actions=int(item["required_actions"]),
                is_secret=bool(item.get("is_secret", False)),
            )
        )
    return achievements


def save_achievements(
    filepath: str,
    achievements: list[Achievement],
) -> None:
    """Сохранить достижения в формате ПР2."""
    _save_records(
        filepath,
        [
            {
                "id": achievement.id,
                "game_id": achievement.game_id,
                "name": achievement.name,
                "required_actions": achievement.required_actions,
                "is_secret": achievement.is_secret,
            }
            for achievement in achievements
        ],
    )


def load_progress(
    filepath: str,
    users: list[User],
    achievements: list[Achievement],
) -> list[Progress]:
    """Загрузить прогресс со ссылками на User и Achievement."""
    users_by_id = {user.id: user for user in users}
    achievements_by_id = {
        achievement.id: achievement for achievement in achievements
    }
    progress_list = []
    for item in _load_records(filepath):
        user = users_by_id.get(int(item["user_id"]))
        achievement = achievements_by_id.get(int(item["achievement_id"]))
        if user is None or achievement is None:
            continue
        progress_list.append(
            Progress(
                id=int(item["id"]),
                user=user,
                achievement=achievement,
                completed_actions=int(item["completed_actions"]),
                record_date=str(item["record_date"]),
            )
        )
    return progress_list


def save_progress(filepath: str, progress_list: list[Progress]) -> None:
    """Сохранить прогресс в формате ПР2."""
    _save_records(
        filepath,
        [
            {
                "id": progress.id,
                "user_id": progress.user_id,
                "achievement_id": progress.achievement_id,
                "completed_actions": progress.completed_actions,
                "record_date": progress.record_date,
            }
            for progress in progress_list
        ],
    )
