from django.http import HttpResponse

from achievements import get_achievement_by_id
from homepage.views import page
from storage import load_achievements, load_games


def achievements(request):
    """Страница со списком всех достижений."""
    games_list = load_games("data/games.json")
    items = ""
    for achievement in load_achievements(
        "data/achievements.json", games_list
    ):
        items += (
            f'<li class="list-group-item">'
            f'<a href="/achievements/{achievement.id}/">'
            f'{achievement}</a></li>'
        )
    content = f"""
    <h1>Достижения</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(
        page("Game Achievement Tracker – достижения", content)
    )


def achievement_detail(request, achievement_id):
    """Страница выбранного достижения."""
    games_list = load_games("data/games.json")
    achievements_list = load_achievements(
        "data/achievements.json", games_list
    )
    achievement = get_achievement_by_id(achievements_list, achievement_id)
    if achievement is None:
        content = """
        <h1 class="text-danger">Достижение не найдено</h1>
        <div class="alert alert-danger mt-3">
            Запрошенное достижение не существует.
        </div>
        <a href="/achievements/" class="btn btn-primary mt-2">
            К списку достижений
        </a>
        """
        return HttpResponse(
            page("Достижение не найдено", content),
            status=404,
        )
    secret = "Да" if achievement.is_secret else "Нет"
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{achievement.name}</h5>
            <p class="card-text">
                <strong>ID:</strong> {achievement.id}
            </p>
            <p class="card-text">
                <strong>Игра:</strong>
                <a href="/games/{achievement.game.id}/">
                    {achievement.game.title}
                </a>
            </p>
            <p class="card-text">
                <strong>Требуется действий:</strong>
                {achievement.required_actions}
            </p>
            <p class="card-text">
                <strong>Секретное:</strong> {secret}
            </p>
            <a href="/achievements/" class="btn btn-outline-secondary mt-2">
                ← к списку достижений
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(achievement.name, content),
        status=200,
    )
