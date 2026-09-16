from dataclasses import dataclass
from typing import Any


@dataclass
class User:
    """Профиль игрока."""

    id: int
    username: str

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "User":
        """Создать пользователя из записи JSON."""
        return cls(id=int(data["id"]), username=str(data["username"]))

    def __str__(self) -> str:
        return f"ID {self.id}: {self.username}"
