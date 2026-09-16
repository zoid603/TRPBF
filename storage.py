import json
import os
from typing import List, Dict, Any


def load_json(filepath: str) -> List[Dict[str, Any]]:
    """Загрузка списка записей из JSON с обработкой ошибок."""
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_json(filepath: str, data: List[Dict[str, Any]]) -> None:
    """Сохранение списка записей в JSON-файл."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
