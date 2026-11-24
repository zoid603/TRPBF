from django.shortcuts import render

from db.queries import get_progress, list_progress, progress_statistics


def progress_list(request):
    """Страница со списком записей прогресса из SQLite."""
    context = {
        "progress_list": list_progress(),
    }
    return render(request, "progress_records/progress_list.html", context)


def progress_detail(request, progress_id):
    """Страница карточки прогресса."""
    record = get_progress(progress_id)
    status = 200 if record is not None else 404
    return render(
        request,
        "progress_records/progress_detail.html",
        {"progress": record},
        status=status,
    )


def statistics(request):
    """Число записей прогресса по каждой игре."""
    context = {
        "statistics": progress_statistics(),
    }
    return render(request, "progress_records/statistics.html", context)
