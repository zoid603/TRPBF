from achievements import (
    add_achievement,
    find_achievements,
    get_achievements_by_game,
    get_achievement_by_id,
    sort_achievements_by_complexity,
)
from models import Achievement, Game


def test_achievement_creation_and_methods() -> None:
    game = Game(1, "DOOM")
    achievements: list[Achievement] = []
    achievement = add_achievement(achievements, game, "Sharpshooter", 50)

    assert achievement.game is game
    assert achievement.game_id == 1
    assert achievement.progress_percent(10) == 20.0
    assert not achievement.is_unlocked(10)
    assert achievement.is_unlocked(50)
    assert "Sharpshooter" in str(achievement)


def test_achievement_search_and_sorting() -> None:
    game = Game(1, "DOOM")
    achievements = [
        Achievement(1, game, "Master BFG", 100),
        Achievement(2, game, "Sharpshooter", 10),
    ]

    assert list(find_achievements(achievements, "bfg")) == [achievements[0]]
    assert get_achievement_by_id(achievements, 2) is achievements[1]
    assert get_achievements_by_game(achievements, game) == achievements
    assert sort_achievements_by_complexity(achievements) == [
        achievements[1],
        achievements[0],
    ]
