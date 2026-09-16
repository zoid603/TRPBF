from dataclasses import dataclass

from .games import Game


@dataclass
class Achievement:
    """Игровое достижение, связанное с игрой."""

    id: int
    game: Game
    name: str
    required_actions: int
    is_secret: bool = False

    @property
    def game_id(self) -> int:
        """Вернуть идентификатор связанной игры."""
        return self.game.id

    def is_unlocked(self, completed_actions: int) -> bool:
        """Проверить, достигнут ли требуемый прогресс."""
        return (
            self.required_actions > 0
            and completed_actions >= self.required_actions
        )

    def progress_percent(self, completed_actions: int) -> float:
        """Рассчитать процент выполнения с ограничением до 100."""
        if self.required_actions <= 0:
            return 0.0
        percent = completed_actions / self.required_actions * 100
        return round(min(percent, 100.0), 2)

    def __str__(self) -> str:
        secret_mark = " [Секретное]" if self.is_secret else ""
        return (
            f"ID {self.id}: [{self.game.title}] {self.name} "
            f"(Требуется: {self.required_actions}){secret_mark}"
        )
