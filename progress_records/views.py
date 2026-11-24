from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import render

from games_app.models import Game
from progress_records.models import Progress


def progress_list(request):
    """Список прогресса: фильтр, поиск, сортировка и страницы."""
    query = request.GET.get("q", "").strip()
    state = request.GET.get("state", "")
    sort = request.GET.get("sort", "date")
    records = Progress.objects.select_related(
        "user",
        "achievement",
        "achievement__game",
    )
    if state == "done":
        records = records.filter(
            completed_actions__gte=F("achievement__required_actions"),
        )
    elif state == "active":
        records = records.filter(completed_actions__gt=0).exclude(
            completed_actions__gte=F("achievement__required_actions"),
        )
    if query:
        records = records.filter(
            Q(user__username__icontains=query)
            | Q(achievement__name__icontains=query),
        )
    if sort == "user":
        records = records.order_by("user__username", "-record_date")
    else:
        records = records.order_by("-record_date", "id")
    paginator = Paginator(records, 5)
    page_obj = paginator.get_page(request.GET.get("page"))
    params = request.GET.copy()
    params.pop("page", None)
    context = {
        "progress_list": page_obj.object_list,
        "page_obj": page_obj,
        "query": query,
        "state": state,
        "sort": sort,
        "querystring": params.urlencode(),
    }
    return render(
        request,
        "progress_records/progress_list.html",
        context,
    )


def progress_detail(request, progress_id):
    """Карточка одной записи прогресса."""
    record = (
        Progress.objects.select_related(
            "user",
            "achievement",
            "achievement__game",
        )
        .filter(pk=progress_id)
        .first()
    )
    status = 200 if record is not None else 404
    return render(
        request,
        "progress_records/progress_detail.html",
        {"progress": record},
        status=status,
    )


def statistics(request):
    """Число записей прогресса по играм и общий итог."""
    rows = (
        Game.objects.annotate(
            progress_count=Count("achievements__progress_records"),
        )
        .order_by("-progress_count", "title")
    )
    total = Progress.objects.aggregate(total=Count("id"))
    return render(
        request,
        "progress_records/statistics.html",
        {"statistics": rows, "total": total["total"]},
    )
