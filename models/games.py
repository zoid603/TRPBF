from dataclasses import dataclass


@dataclass
class Game:
    """Игровая сущность каталога."""

    id: int
    title: str

    def __str__(self) -> str:
        return f"ID {self.id}: {self.title}"
