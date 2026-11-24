from django.shortcuts import render

from db.queries import (
    get_achievement,
    list_achievements,
    open_achievements,
)


def achievements(request):
    """Страница со списком достижений из SQLite."""
    context = {
        "achievements_list": list_achievements(),
    }
    return render(request, "achievement/achievements.html", context)


def achievement_detail(request, achievement_id):
    """Страница выбранного достижения."""
    achievement = get_achievement(achievement_id)
    status = 200 if achievement is not None else 404
    return render(
        request,
        "achievement/achievement_detail.html",
        {"achievement": achievement},
        status=status,
    )


def open_on_date(request):
    """Достижения, которые ещё не получены на выбранную дату."""
    on_date = request.GET.get("date", "")
    achievements_list = []
    if on_date:
        achievements_list = open_achievements(on_date)
    context = {
        "on_date": on_date,
        "achievements_list": achievements_list,
    }
    return render(request, "achievement/open.html", context)
