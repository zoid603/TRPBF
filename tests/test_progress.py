import pytest

from models import Achievement, Game, Progress, User
from progress import format_achievement_summary, record_progress


@pytest.mark.smoke
@pytest.mark.parametrize(
    ("completed_actions", "expected_percent", "expected_status"),
    [
        (0, 0.0, "Не начато"),
        (10, 20.0, "В процессе"),
        (50, 100.0, "Получено"),
    ],
)
def test_progress_creation_and_status(
    completed_actions: int,
    expected_percent: float,
    expected_status: str,
) -> None:
    game = Game(1, "DOOM")
    user = User(1, "PlayerOne")
    achievement = Achievement(1, game, "Sharpshooter", 50)
    progress_list: list[Progress] = []

    progress = record_progress(
        progress_list,
        user,
        achievement,
        completed_actions,
        "2026-09-15",
    )

    assert progress.percent() == expected_percent
    assert progress.status() == expected_status
    assert progress.user is user
    assert progress.achievement is achievement
    assert f"{expected_percent}%" in format_achievement_summary(progress)


@pytest.mark.unit
def test_progress_update_reuses_existing_object() -> None:
    game = Game(1, "DOOM")
    user = User(1, "PlayerOne")
    achievement = Achievement(1, game, "Sharpshooter", 50)
    progress_list: list[Progress] = []
    progress = record_progress(
        progress_list,
        user,
        achievement,
        10,
        "2026-09-15",
    )

    updated = record_progress(
        progress_list,
        user,
        achievement,
        50,
        "2026-09-16",
    )

    assert updated is progress
    assert len(progress_list) == 1
    assert updated.status() == "Получено"
    assert updated.record_date == "2026-09-16"
