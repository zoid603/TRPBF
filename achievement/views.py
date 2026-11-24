import re

from django.db.models import F, Q
from django.shortcuts import render

from achievement.models import Achievement
from progress_records.models import Progress

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def _optional_int(value):
    """Вернуть целое из строки запроса или None."""
    if value in (None, ""):
        return None
    try:
        return int(value)
    except ValueError:
        return None


def achievements(request):
    """Список достижений с фильтром и поиском."""
    query = request.GET.get("q", "").strip()
    secret = request.GET.get("secret", "")
    min_actions = _optional_int(request.GET.get("min_actions"))
    items = Achievement.objects.select_related("game")
    if secret == "1":
        items = items.filter(is_secret=True)
    elif secret == "0":
        items = items.exclude(is_secret=True)
    if min_actions is not None:
        items = items.filter(
            required_actions__gte=min_actions,
            game__title__isnull=False,
        )
    if query:
        items = items.filter(
            Q(name__icontains=query) | Q(game__title__icontains=query),
        )
    context = {
        "achievements_list": items.order_by("name"),
        "query": query,
        "secret": secret,
        "min_actions": request.GET.get("min_actions", ""),
    }
    return render(request, "achievement/achievements.html", context)


def achievement_detail(request, achievement_id):
    """Карточка достижения."""
    achievement = (
        Achievement.objects.select_related("game")
        .filter(pk=achievement_id)
        .first()
    )
    status = 200 if achievement is not None else 404
    return render(
        request,
        "achievement/achievement_detail.html",
        {"achievement": achievement},
        status=status,
    )


def open_on_date(request):
    """Достижения, не полученные на выбранную дату."""
    on_date = request.GET.get("date", "")
    items = []
    if _DATE.match(on_date):
        obtained_ids = Progress.objects.filter(
            record_date__lte=on_date,
            completed_actions__gte=F("achievement__required_actions"),
        ).values("achievement_id")
        items = (
            Achievement.objects.select_related("game")
            .exclude(id__in=obtained_ids)
            .order_by("game__title", "name")
        )
    elif on_date:
        on_date = ""
    return render(
        request,
        "achievement/open.html",
        {"on_date": on_date, "achievements_list": items},
    )
