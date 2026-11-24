from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Game(models.Model):
    """Игра каталога."""

    title = models.CharField("название", max_length=200)
    slug = models.SlugField("адрес", max_length=80, unique=True)

    class Meta:
        db_table = "games"
        ordering = ["title"]
        verbose_name = "игра"
        verbose_name_plural = "игры"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        """Адрес страницы игры по слагу."""
        return reverse("games_app:detail", kwargs={"game_slug": self.slug})
