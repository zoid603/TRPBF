from games_app.models import Game


def catalog(request):
    """Общее число игр для подвала всех страниц."""
    return {"catalog_game_count": Game.objects.count()}
