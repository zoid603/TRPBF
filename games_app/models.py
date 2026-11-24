from django.db import models


class Game(models.Model):
    """Игра каталога."""

    title = models.CharField("название", max_length=200)

    class Meta:
        db_table = "games"
        ordering = ["title"]
        verbose_name = "игра"
        verbose_name_plural = "игры"

    def __str__(self):
        return self.title
