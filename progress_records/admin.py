from django.contrib import admin

from .models import Progress


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    """Прогресс: связанные игрок и достижение, фильтр и поиск."""

    list_display = (
        "user",
        "achievement",
        "completed_actions",
        "record_date",
        "is_started",
    )
    list_filter = ("record_date", "achievement__game", "is_started")
    search_fields = ("user__username", "achievement__name")
    autocomplete_fields = ("user", "achievement")
    list_select_related = ("user", "achievement", "achievement__game")
    ordering = ("-record_date",)
