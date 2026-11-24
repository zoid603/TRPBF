from django.db import migrations, models
from django.utils.text import slugify


def fill_slugs(apps, schema_editor):
    """Заполнить слаг из названия игры."""
    game_model = apps.get_model("games_app", "Game")
    for game in game_model.objects.all():
        game.slug = slugify(game.title) or f"game-{game.pk}"
        game.save(update_fields=["slug"])


class Migration(migrations.Migration):

    dependencies = [
        ("games_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="game",
            name="slug",
            field=models.SlugField(
                max_length=80,
                null=True,
                unique=True,
                verbose_name="адрес",
            ),
        ),
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="game",
            name="slug",
            field=models.SlugField(
                max_length=80,
                unique=True,
                verbose_name="адрес",
            ),
        ),
    ]
