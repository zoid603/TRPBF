from django.db import models


class Progress(models.Model):
    """Прогресс игрока по одному достижению."""

    user = models.ForeignKey(
        "players.Player",
        verbose_name="игрок",
        on_delete=models.CASCADE,
        related_name="progress_records",
        db_column="user_id",
    )
    achievement = models.ForeignKey(
        "achievement.Achievement",
        verbose_name="достижение",
        on_delete=models.CASCADE,
        related_name="progress_records",
        db_column="achievement_id",
    )
    completed_actions = models.PositiveIntegerField("выполнено действий")
    record_date = models.CharField("дата фиксации", max_length=10)

    class Meta:
        db_table = "progress"
        ordering = ["-record_date", "id"]
        verbose_name = "прогресс"
        verbose_name_plural = "прогресс"

    def __str__(self):
        return f"{self.user} — {self.achievement}"

    def percent(self):
        """Процент выполнения, не больше 100."""
        required = self.achievement.required_actions
        if required <= 0:
            return 0.0
        value = self.completed_actions / required * 100
        return round(min(value, 100.0), 2)

    def status(self):
        """Текстовый статус записи."""
        required = self.achievement.required_actions
        if required > 0 and self.completed_actions >= required:
            return "Получено"
        if self.completed_actions > 0:
            return "В процессе"
        return "Не начато"
