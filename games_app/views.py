from django.shortcuts import render

from achievements import get_achievements_by_game
from games import get_game_by_id
from storage import load_achievements, load_games


def games(request):
    """Страница со списком игр каталога."""
    games_list = load_games("data/games.json")
    achievements = load_achievements("data/achievements.json", games_list)
    games_with_counts = []
    for game in games_list:
        count = len(get_achievements_by_game(achievements, game))
        games_with_counts.append({
            "game": game,
            "count": count,
        })
    context = {
        "games_list": games_list,
        "games_with_counts": games_with_counts,
    }
    return render(request, "games_app/games.html", context)


def game_detail(request, game_id):
    """Страница выбранной игры с её достижениями."""
    games_list = load_games("data/games.json")
    game = get_game_by_id(games_list, game_id)
    if game is None:
        context = {"game": None}
        return render(
            request,
            "games_app/game_detail.html",
            context,
            status=404,
        )

    achievements = load_achievements("data/achievements.json", games_list)
    game_achievements = get_achievements_by_game(achievements, game)
    context = {
        "game": game,
        "game_achievements": game_achievements,
    }
    return render(
        request,
        "games_app/game_detail.html",
        context,
        status=200,
    )
