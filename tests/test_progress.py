import pytest
from datetime import date
from progress import (
    calculate_progress_percent,
    check_unlock_status,
    record_progress,
    get_user_progress,
)


@pytest.mark.unit
@pytest.mark.parametrize(
    "completed, total, expected",
    [
        (10, 50, 20.0),
        (50, 50, 100.0),
        (60, 50, 100.0),
        (0, 50, 0.0),
        (10, 0, 0.0),
        (10, -5, 0.0),
    ],
)
def test_calculate_progress_percent(
    completed: int, total: int, expected: float
):
    """1. Параметризованный расчет процента с граничными случаями."""
    assert calculate_progress_percent(completed, total) == expected


@pytest.mark.unit
@pytest.mark.parametrize(
    "completed, total, expected_status",
    [
        (0, 10, "Не начато"),
        (1, 10, "В процессе"),
        (9, 10, "В процессе"),
        (10, 10, "Получено"),
        (15, 10, "Получено"),
    ],
)
def test_check_unlock_status_all_variants(
    completed: int, total: int, expected_status: str
):
    """2. Параметризованная проверка всех статусов разблокировки."""
    assert check_unlock_status(completed, total) == expected_status


@pytest.mark.smoke
def test_record_progress_insert_and_update():
    """3. Создание новой записи прогресса и обновление существующей."""
    progress_list = []
    day = date(2026, 9, 15)

    item = record_progress(
        progress_list, user_id=1, achievement_id=1,
        completed_actions=10, record_date=day
    )
    assert len(progress_list) == 1
    assert item["completed_actions"] == 10

    updated_item = record_progress(
        progress_list, user_id=1, achievement_id=1,
        completed_actions=30, record_date=day
    )
    assert len(progress_list) == 1
    assert updated_item["completed_actions"] == 30


@pytest.mark.unit
@pytest.mark.parametrize(
    "target_user, target_ach, expected_completed",
    [
        (1, 1, 5),
        (2, 1, 10),
        (1, 2, None),
        (3, 1, None),
    ],
)
def test_get_user_progress_filtering(
    target_user: int, target_ach: int, expected_completed
):
    """4. Параметризованная выборка прогресса по пользователю и ачивке."""
    progress_list = [
        {"id": 1, "user_id": 1, "achievement_id": 1, "completed_actions": 5},
        {"id": 2, "user_id": 2, "achievement_id": 1, "completed_actions": 10},
    ]
    prog = get_user_progress(
        progress_list, user_id=target_user, achievement_id=target_ach
    )
    if expected_completed is None:
        assert prog is None
    else:
        assert prog is not None
        assert prog["completed_actions"] == expected_completed
