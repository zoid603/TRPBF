from dataclasses import dataclass

from .achievements import Achievement
from .users import User


@dataclass
class Progress:
    """Прогресс пользователя по конкретному достижению."""

    id: int
    user: User
    achievement: Achievement
    completed_actions: int
    record_date: str

    @property
    def user_id(self) -> int:
        """Вернуть идентификатор пользователя."""
        return self.user.id

    @property
    def achievement_id(self) -> int:
        """Вернуть идентификатор достижения."""
        return self.achievement.id

    def update(self, completed_actions: int, record_date: str) -> None:
        """Обновить количество выполненных действий и дату."""
        self.completed_actions = completed_actions
        self.record_date = record_date

    def percent(self) -> float:
        """Вернуть процент выполнения достижения."""
        return self.achievement.progress_percent(self.completed_actions)

    def status(self) -> str:
        """Вернуть текстовый статус прогресса."""
        if self.achievement.is_unlocked(self.completed_actions):
            return "Получено"
        if self.completed_actions > 0:
            return "В процессе"
        return "Не начато"

    def __str__(self) -> str:
        return (
            f"{self.user.username}: {self.achievement.name} - "
            f"{self.percent()}% ({self.status()})"
        )
