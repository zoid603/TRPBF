from django.shortcuts import render

from db.queries import get_game, list_game_achievements, list_games


def games(request):
    """Страница со списком игр из SQLite."""
    games_with_counts = list_games()
    context = {
        "games_list": [item["game"] for item in games_with_counts],
        "games_with_counts": games_with_counts,
    }
    return render(request, "games_app/games.html", context)


def game_detail(request, game_id):
    """Страница выбранной игры и её достижений."""
    game = get_game(game_id)
    if game is None:
        return render(
            request,
            "games_app/game_detail.html",
            {"game": None},
            status=404,
        )
    context = {
        "game": game,
        "game_achievements": list_game_achievements(game_id),
    }
    return render(
        request,
        "games_app/game_detail.html",
        context,
        status=200,
    )
