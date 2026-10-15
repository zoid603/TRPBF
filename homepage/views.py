from django.shortcuts import render

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
    return render(
        request,
        "404.html",
        {
            "message": _not_found_message(request.path),
            "path": request.path,
        },
        status=404,
    )


def index(request):
    """Главная страница приложения."""
    return render(request, "homepage/index.html")
