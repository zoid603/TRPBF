import json
from pathlib import Path

from django.core.management.base import BaseCommand

from django.utils.text import slugify

from achievement.models import Achievement
from games_app.models import Game
from players.models import Player
from progress_records.models import Progress

BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"


def _load(name):
    with (DATA_DIR / name).open(encoding="utf-8") as source:
        return json.load(source)


class Command(BaseCommand):
    """Перенести каталог из JSON в таблицы Django ORM."""

    help = "Загрузить игры, игроков, достижения и прогресс из data/*.json"

    def handle(self, *args, **options):
        games = _load("games.json")
        users = _load("users.json")
        achievements = _load("achievements.json")
        records = _load("progress.json")

        game_ids = {item["id"] for item in games}
        user_ids = {item["id"] for item in users}
        achievement_ids = {item["id"] for item in achievements}
        progress_ids = {item["id"] for item in records}

        Progress.objects.exclude(id__in=progress_ids).delete()
        Achievement.objects.exclude(id__in=achievement_ids).delete()
        Player.objects.exclude(id__in=user_ids).delete()
        Game.objects.exclude(id__in=game_ids).delete()

        for item in games:
            Game.objects.update_or_create(
                id=item["id"],
                defaults={
                    "title": item["title"],
                    "slug": slugify(item["title"]),
                },
            )
        for item in users:
            Player.objects.update_or_create(
                id=item["id"],
                defaults={"username": item["username"]},
            )
        for item in achievements:
            Achievement.objects.update_or_create(
                id=item["id"],
                defaults={
                    "game_id": item["game_id"],
                    "name": item["name"],
                    "required_actions": item["required_actions"],
                    "is_secret": item["is_secret"],
                },
            )
        for item in records:
            Progress.objects.update_or_create(
                id=item["id"],
                defaults={
                    "user_id": item["user_id"],
                    "achievement_id": item["achievement_id"],
                    "completed_actions": item["completed_actions"],
                    "record_date": item["record_date"],
                },
            )
        self.stdout.write(self.style.SUCCESS("Каталог загружен в ORM"))
