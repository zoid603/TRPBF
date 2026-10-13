from django.http import HttpResponse

from achievements import get_achievements_by_game
from games import get_game_by_id
from homepage.views import page
from storage import load_achievements, load_games


def games(request):
    """Страница со списком игр каталога."""
    games_list = load_games("data/games.json")
    achievements = load_achievements("data/achievements.json", games_list)
    items = ""
    for game in games_list:
        count = len(get_achievements_by_game(achievements, game))
        text = f"{game} (Достижений: {count})"
        items += (
            f'<li class="list-group-item">'
            f'<a href="/games/{game.id}/">{text}</a>'
            f'</li>'
        )
    content = f"""
    <h1>Игры</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Game Achievement Tracker – игры", content))


def game_detail(request, game_id):
    """Страница выбранной игры с её достижениями."""
    games_list = load_games("data/games.json")
    game = get_game_by_id(games_list, game_id)
    if game is None:
        content = """
        <h1 class="text-danger">Игра не найдена</h1>
        <div class="alert alert-danger mt-3">
            Запрошенная игра не существует.
        </div>
        <a href="/games/" class="btn btn-primary mt-2">К списку игр</a>
        """
        return HttpResponse(
            page("Игра не найдена", content),
            status=404,
        )
    achievements = load_achievements("data/achievements.json", games_list)
    game_achievements = get_achievements_by_game(achievements, game)
    items = ""
    for achievement in game_achievements:
        items += (
            f'<li class="list-group-item">'
            f'<a href="/achievements/{achievement.id}/">'
            f'{achievement}</a></li>'
        )
    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{game.title}</h5>
            <p class="card-text">
                <strong>ID:</strong> {game.id}
            </p>
            <p class="card-text">
                <strong>Достижений:</strong> {len(game_achievements)}
            </p>
            <ul class="list-group">{items}</ul>
            <a href="/games/" class="btn btn-outline-secondary mt-2">
                ← к списку игр
            </a>
        </div>
    </div>
    """
    return HttpResponse(
        page(game.title, content),
        status=200,
    )
