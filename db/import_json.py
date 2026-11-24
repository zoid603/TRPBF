import json
import sqlite3
from pathlib import Path

from db.database import DB_PATH

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"
DATA_DIR = BASE_DIR / "data"


def _load(name):
    """Прочитать JSON-файл каталога data."""
    with (DATA_DIR / name).open(encoding="utf-8") as source:
        return json.load(source)


def import_json():
    """Создать таблицы и перенести данные из JSON в SQLite."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    try:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("DELETE FROM progress")
        connection.execute("DELETE FROM achievements")
        connection.execute("DELETE FROM users")
        connection.execute("DELETE FROM games")
        for game in _load("games.json"):
            connection.execute(
                "INSERT INTO games (id, title) VALUES (?, ?)",
                (game["id"], game["title"]),
            )
        for user in _load("users.json"):
            connection.execute(
                "INSERT INTO users (id, username) VALUES (?, ?)",
                (user["id"], user["username"]),
            )
        for item in _load("achievements.json"):
            connection.execute(
                """
                INSERT INTO achievements (
                    id, game_id, name, required_actions, is_secret
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item["game_id"],
                    item["name"],
                    item["required_actions"],
                    1 if item["is_secret"] else 0,
                ),
            )
        for item in _load("progress.json"):
            connection.execute(
                """
                INSERT INTO progress (
                    id, user_id, achievement_id,
                    completed_actions, record_date
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (
                    item["id"],
                    item["user_id"],
                    item["achievement_id"],
                    item["completed_actions"],
                    item["record_date"],
                ),
            )
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    import_json()
    print(f"Данные импортированы в {DB_PATH}")
