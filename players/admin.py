from django.contrib import admin

from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Игроки каталога."""

    list_display = ("username",)
    search_fields = ("username",)
    ordering = ("username",)
