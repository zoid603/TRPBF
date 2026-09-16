import pytest
from achievements import (
    add_achievement,
    get_achievement_by_id,
    find_achievements,
    sort_achievements_by_complexity,
)


@pytest.mark.smoke
def test_add_achievement_success():
    """1. Проверка создания достижения с привязкой к игре."""
    achs = []
    ach = add_achievement(
        achs, game_id=1, name="Меткий стрелок",
        required_actions=50, is_secret=False
    )
    assert len(achs) == 1
    assert ach["id"] == 1
    assert ach["game_id"] == 1
    assert ach["name"] == "Меткий стрелок"
    assert ach["is_secret"] is False


@pytest.mark.unit
def test_get_achievement_by_id():
    """2. Поиск достижения по ID."""
    achs = [
        {
            "id": 1, "game_id": 1, "name": "Первая кровь",
            "required_actions": 1, "is_secret": False
        }
    ]
    found = get_achievement_by_id(achs, 1)
    assert found is not None
    assert found["name"] == "Первая кровь"
    assert get_achievement_by_id(achs, 42) is None


@pytest.mark.unit
@pytest.mark.parametrize(
    "query, expected_ids",
    [
        ("мастер", {1, 3}),
        ("меткий", {2}),
        ("BFG", {1}),
        ("секрет", set()),
    ],
)
def test_find_achievements_parametrized(query: str, expected_ids: set):
    """3. Параметризованный поиск ачивок через генератор."""
    achs = [
        {"id": 1, "name": "Мастер BFG"},
        {"id": 2, "name": "Меткий стрелок"},
        {"id": 3, "name": "Мастер меча"},
    ]
    results = list(find_achievements(achs, query))
    assert {a["id"] for a in results} == expected_ids


@pytest.mark.unit
def test_sort_achievements_by_complexity():
    """4. Сортировка достижений по возрастанию требуемых действий."""
    achs = [
        {"id": 1, "required_actions": 100},
        {"id": 2, "required_actions": 5},
        {"id": 3, "required_actions": 50},
    ]
    sorted_list = sort_achievements_by_complexity(achs)
    assert [a["required_actions"] for a in sorted_list] == [5, 50, 100]
