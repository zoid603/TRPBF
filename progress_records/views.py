from django.shortcuts import render

from progress import get_progress_by_id
from storage import load_achievements, load_games, load_progress, load_users


def progress_list(request):
    """Страница со списком записей прогресса."""
    games_list = load_games("data/games.json")
    users_list = load_users("data/users.json")
    achievements_list = load_achievements(
        "data/achievements.json", games_list
    )
    records = load_progress(
        "data/progress.json", users_list, achievements_list
    )
    context = {
        "progress_list": records,
    }
    return render(request, "progress_records/progress_list.html", context)


def progress_detail(request, progress_id):
    """Страница карточки прогресса."""
    games_list = load_games("data/games.json")
    users_list = load_users("data/users.json")
    achievements_list = load_achievements(
        "data/achievements.json", games_list
    )
    records = load_progress(
        "data/progress.json", users_list, achievements_list
    )
    record = get_progress_by_id(records, progress_id)
    if record is None:
        context = {"progress": None}
        return render(
            request,
            "progress_records/progress_detail.html",
            context,
            status=404,
        )
    context = {
        "progress": record,
    }
    return render(
        request,
        "progress_records/progress_detail.html",
        context,
        status=200,
    )
