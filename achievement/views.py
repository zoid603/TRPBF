from django.shortcuts import render

from achievements import get_achievement_by_id
from storage import load_achievements, load_games


def achievements(request):
    """Страница со списком всех достижений."""
    games_list = load_games("data/games.json")
    achievements_list = load_achievements(
        "data/achievements.json", games_list
    )
    context = {
        "achievements_list": achievements_list,
    }
    return render(request, "achievement/achievements.html", context)


def achievement_detail(request, achievement_id):
    """Страница выбранного достижения."""
    games_list = load_games("data/games.json")
    achievements_list = load_achievements(
        "data/achievements.json", games_list
    )
    achievement = get_achievement_by_id(achievements_list, achievement_id)
    if achievement is None:
        context = {"achievement": None}
        return render(
            request,
            "achievement/achievement_detail.html",
            context,
            status=404,
        )
    context = {
        "achievement": achievement,
    }
    return render(
        request,
        "achievement/achievement_detail.html",
        context,
        status=200,
    )
