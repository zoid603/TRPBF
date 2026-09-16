from models import Achievement, Game, Progress, User
from progress import format_achievement_summary, record_progress


def test_progress_creation_and_status() -> None:
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

    assert progress.percent() == 20.0
    assert progress.status() == "В процессе"
    assert progress.user is user
    assert progress.achievement is achievement
    assert "20.0%" in format_achievement_summary(progress)


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
