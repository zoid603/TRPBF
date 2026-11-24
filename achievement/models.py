from django.db import models


class Achievement(models.Model):
    """Достижение, относящееся к одной игре."""

    game = models.ForeignKey(
        "games_app.Game",
        verbose_name="игра",
        on_delete=models.CASCADE,
        related_name="achievements",
        db_column="game_id",
    )
    name = models.CharField("название", max_length=200)
    required_actions = models.PositiveIntegerField("нужно действий")
    is_secret = models.BooleanField("секретное", default=False)

    class Meta:
        db_table = "achievements"
        ordering = ["name"]
        verbose_name = "достижение"
        verbose_name_plural = "достижения"

    def __str__(self):
        return self.name
