from django.http import HttpResponse
from django.template.loader import render_to_string


def page(title, content):
    """Собрать единый HTML-каркас страницы с Bootstrap 5.3."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body>
    <nav class="nav">
        <a class="nav-link" href="/">Главная</a>
        <a class="nav-link" href="/games/">Игры</a>
        <a class="nav-link" href="/achievements/">Достижения</a>
        <a class="nav-link" href="/progress/">Прогресс</a>
    </nav>
    <main class="container">{content}</main>
</body>
</html>"""


_ID_FIELD_NAMES = {
    "games": "игры",
    "achievements": "достижения",
    "progress": "прогресса",
}


def _not_found_message(path):
    """Подобрать текст страницы 404 по запрошенному адресу."""
    parts = [part for part in path.split("/") if part]
    if len(parts) == 2:
        section, value = parts
        field = _ID_FIELD_NAMES.get(section)
        if field is not None and not value.isdigit():
            return (
                f"ID {field} должен быть целым числом, "
                f"а получено «{value}»."
            )
    return "Запрошенный адрес не существует."


def page_not_found(request, exception):
    """Обработчик 404 - кастомная страница."""
    content = render_to_string(
        "404.html",
        {
            "message": _not_found_message(request.path),
            "path": request.path,
        },
    )
    return HttpResponse(content, status=404)


def index(request):
    """Главная страница приложения."""
    content = """
    <h1 class="display-4">Game Achievement Tracker</h1>
    <p class="lead">Трекер игровых достижений.</p>
    <p>Основные разделы:</p>
    <a href="/games/" class="btn btn-primary me-2">Игры</a>
    <a href="/achievements/" class="btn btn-secondary me-2">
        Достижения
    </a>
    <a href="/progress/" class="btn btn-outline-primary">Прогресс</a>
    """
    return HttpResponse(page("Game Achievement Tracker", content))
