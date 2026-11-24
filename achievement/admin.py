from django.contrib import admin

from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    """Достижения с фильтром по игре и признаку секретности."""

    list_display = ("name", "game", "required_actions", "is_secret")
    list_filter = ("is_secret", "game")
    search_fields = ("name", "game__title")
    autocomplete_fields = ("game",)
    list_select_related = ("game",)
