from django.db import models


class Player(models.Model):
    """Игрок каталога. Это не учётная запись Django."""

    username = models.CharField("имя", max_length=150)

    class Meta:
        db_table = "users"
        ordering = ["username"]
        verbose_name = "игрок"
        verbose_name_plural = "игроки"

    def __str__(self):
        return self.username
