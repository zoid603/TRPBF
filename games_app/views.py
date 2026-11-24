from django.db.models import Count
from django.shortcuts import render

from games_app.models import Game


def games(request):
    """Список игр: поиск по названию и сортировка."""
    query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "title")
    items = Game.objects.annotate(
        achievements_count=Count("achievements"),
    )
    if query:
        items = items.filter(title__icontains=query)
    if sort == "count":
        items = items.order_by("-achievements_count", "title")
    else:
        items = items.order_by("title", "id")
    games_with_counts = [
        {"game": game, "count": game.achievements_count}
        for game in items
    ]
    context = {
        "games_list": [item["game"] for item in games_with_counts],
        "games_with_counts": games_with_counts,
        "query": query,
        "sort": sort,
    }
    return render(request, "games_app/games.html", context)


def game_detail(request, game_id):
    """Страница игры и её достижений."""
    game = (
        Game.objects.prefetch_related("achievements")
        .filter(pk=game_id)
        .first()
    )
    achievements = []
    if game is not None:
        achievements = game.achievements.all().order_by("name")
    status = 200 if game is not None else 404
    return render(
        request,
        "games_app/game_detail.html",
        {"game": game, "game_achievements": achievements},
        status=status,
    )
