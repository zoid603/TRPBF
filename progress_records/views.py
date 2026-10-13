from django.http import HttpResponse

from homepage.views import page
from progress import get_progress_by_id
from storage import load_achievements, load_games, load_progress, load_users

_STATUS_BADGES = {
    "Получено": "bg-success",
    "В процессе": "bg-warning",
    "Не начато": "bg-secondary",
}


def _badge(status):
    """Вернуть класс бейджа Bootstrap для статуса прогресса."""
    return _STATUS_BADGES.get(status, "bg-secondary")


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
    items = ""
    for record in records:
        text = (
            f"{record.user.username}: {record.achievement.name} "
            f"- {record.percent()}%"
        )
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/progress/{record.id}/">{text}</a>
            <span class="badge {_badge(record.status())}">
                {record.status()}
            </span>
        </li>
        """
    content = f"""
    <h1>Прогресс игроков</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(
        page("Game Achievement Tracker – прогресс", content)
    )


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
        content = """
        <h1 class="text-danger">Прогресс не найден</h1>
        <a href="/progress/" class="btn btn-outline-secondary">
            ← к списку прогресса
        </a>
        """
        return HttpResponse(
            page("Прогресс не найден", content),
            status=404,
        )
    badge = _badge(record.status())
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">
                {record.user.username}
            </h5>
            <p class="card-text">
                Игра: {record.achievement.game.title}
            </p>
            <p class="card-text">
                Достижение: {record.achievement.name}
            </p>
            <p class="card-text">
                Прогресс: {record.percent()}%
                <span class="badge {badge}">
                    {record.status()}
                </span>
            </p>
            <p class="card-text">
                Дата фиксации: {record.record_date}
            </p>
            <a href="/progress/" class="btn btn-outline-secondary">
                ← к списку прогресса
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(f"Прогресс №{record.id}", content),
        status=200,
    )
