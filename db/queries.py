from types import SimpleNamespace

from db.database import fetch_all, fetch_one


def _percent(completed, required):
    """Процент выполнения достижения, не больше 100."""
    if required <= 0:
        return 0.0
    percent = completed / required * 100
    return round(min(percent, 100.0), 2)


def _status(completed, required):
    """Текстовый статус прогресса по числу действий."""
    if required > 0 and completed >= required:
        return "Получено"
    if completed > 0:
        return "В процессе"
    return "Не начато"


def _game(row):
    return SimpleNamespace(id=row["id"], title=row["title"])


def _achievement(row):
    return SimpleNamespace(
        id=row["id"],
        name=row["name"],
        required_actions=row["required_actions"],
        is_secret=bool(row["is_secret"]),
        game=SimpleNamespace(
            id=row["game_id"],
            title=row["game_title"],
        ),
    )


def _progress(row):
    required = row["required_actions"]
    completed = row["completed_actions"]
    achievement = SimpleNamespace(
        id=row["achievement_id"],
        name=row["achievement_name"],
        required_actions=required,
        is_secret=bool(row["is_secret"]),
        game=SimpleNamespace(
            id=row["game_id"],
            title=row["game_title"],
        ),
    )
    return SimpleNamespace(
        id=row["id"],
        completed_actions=completed,
        record_date=row["record_date"],
        percent=_percent(completed, required),
        status=_status(completed, required),
        user=SimpleNamespace(
            id=row["user_id"],
            username=row["username"],
        ),
        achievement=achievement,
    )


def list_games():
    """Список игр и число достижений у каждой."""
    rows = fetch_all(
        """
        SELECT
            games.id,
            games.title,
            COUNT(achievements.id) AS achievements_count
        FROM games
        LEFT JOIN achievements ON achievements.game_id = games.id
        GROUP BY games.id, games.title
        ORDER BY games.title
        """
    )
    return [
        {
            "game": _game(row),
            "count": row["achievements_count"],
        }
        for row in rows
    ]


def get_game(game_id):
    """Найти игру по идентификатору."""
    row = fetch_one(
        "SELECT id, title FROM games WHERE id = ?",
        (game_id,),
    )
    if row is None:
        return None
    return _game(row)


def list_game_achievements(game_id):
    """Достижения выбранной игры."""
    rows = fetch_all(
        """
        SELECT
            achievements.id,
            achievements.name,
            achievements.required_actions,
            achievements.is_secret,
            games.id AS game_id,
            games.title AS game_title
        FROM achievements
        JOIN games ON games.id = achievements.game_id
        WHERE achievements.game_id = ?
        ORDER BY achievements.name
        """,
        (game_id,),
    )
    return [_achievement(row) for row in rows]


def list_achievements():
    """Все достижения вместе с игрой."""
    rows = fetch_all(
        """
        SELECT
            achievements.id,
            achievements.name,
            achievements.required_actions,
            achievements.is_secret,
            games.id AS game_id,
            games.title AS game_title
        FROM achievements
        JOIN games ON games.id = achievements.game_id
        ORDER BY achievements.name
        """
    )
    return [_achievement(row) for row in rows]


def get_achievement(achievement_id):
    """Найти достижение по идентификатору."""
    row = fetch_one(
        """
        SELECT
            achievements.id,
            achievements.name,
            achievements.required_actions,
            achievements.is_secret,
            games.id AS game_id,
            games.title AS game_title
        FROM achievements
        JOIN games ON games.id = achievements.game_id
        WHERE achievements.id = ?
        """,
        (achievement_id,),
    )
    if row is None:
        return None
    return _achievement(row)


def list_progress():
    """Записи прогресса со связанными игроком, достижением и игрой."""
    rows = fetch_all(
        """
        SELECT
            progress.id,
            progress.completed_actions,
            progress.record_date,
            users.id AS user_id,
            users.username,
            achievements.id AS achievement_id,
            achievements.name AS achievement_name,
            achievements.required_actions,
            achievements.is_secret,
            games.id AS game_id,
            games.title AS game_title
        FROM progress
        JOIN users ON users.id = progress.user_id
        JOIN achievements
            ON achievements.id = progress.achievement_id
        JOIN games ON games.id = achievements.game_id
        ORDER BY progress.record_date DESC, progress.id
        """
    )
    return [_progress(row) for row in rows]


def get_progress(progress_id):
    """Найти запись прогресса по идентификатору."""
    row = fetch_one(
        """
        SELECT
            progress.id,
            progress.completed_actions,
            progress.record_date,
            users.id AS user_id,
            users.username,
            achievements.id AS achievement_id,
            achievements.name AS achievement_name,
            achievements.required_actions,
            achievements.is_secret,
            games.id AS game_id,
            games.title AS game_title
        FROM progress
        JOIN users ON users.id = progress.user_id
        JOIN achievements
            ON achievements.id = progress.achievement_id
        JOIN games ON games.id = achievements.game_id
        WHERE progress.id = ?
        """,
        (progress_id,),
    )
    if row is None:
        return None
    return _progress(row)


def open_achievements(on_date):
    """Достижения, которые ещё не получены на выбранную дату."""
    rows = fetch_all(
        """
        SELECT
            achievements.id,
            achievements.name,
            achievements.required_actions,
            achievements.is_secret,
            games.id AS game_id,
            games.title AS game_title
        FROM achievements
        JOIN games ON games.id = achievements.game_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM progress
            WHERE progress.achievement_id = achievements.id
              AND progress.completed_actions
                  >= achievements.required_actions
              AND progress.record_date <= ?
        )
        ORDER BY games.title, achievements.name
        """,
        (on_date,),
    )
    return [_achievement(row) for row in rows]


def progress_statistics():
    """Число записей прогресса по каждой игре."""
    return fetch_all(
        """
        SELECT
            games.title AS game_title,
            COUNT(progress.id) AS progress_count
        FROM games
        LEFT JOIN achievements ON achievements.game_id = games.id
        LEFT JOIN progress
            ON progress.achievement_id = achievements.id
        GROUP BY games.id, games.title
        ORDER BY progress_count DESC, games.title
        """
    )
