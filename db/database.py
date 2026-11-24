import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "data" / "tracker.sqlite"


def get_connection():
    """Открыть соединение SQLite с доступом к полям по имени."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def fetch_all(sql, params=()):
    """Выполнить запрос и вернуть все строки."""
    connection = get_connection()
    try:
        return connection.execute(sql, params).fetchall()
    finally:
        connection.close()


def fetch_one(sql, params=()):
    """Выполнить запрос и вернуть одну строку или None."""
    connection = get_connection()
    try:
        return connection.execute(sql, params).fetchone()
    finally:
        connection.close()
