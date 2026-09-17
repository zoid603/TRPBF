import logging
import os
from datetime import date

from achievements import (
    add_achievement,
    find_achievements,
    get_achievement_by_id,
    get_achievements_by_game,
)
from games import add_game, get_game_by_id
from models import Achievement, Game, Progress, User
from progress import (
    format_achievement_summary,
    get_user_progress,
    record_progress,
)
from storage import (
    load_achievements,
    load_games,
    load_progress,
    load_users,
    save_achievements,
    save_games,
    save_progress,
    save_users,
)
from users import add_user, get_user_by_id, get_user_by_username, show_users
from utils import input_date, input_int

USERS_FILE = "data/users.json"
GAMES_FILE = "data/games.json"
ACHIEVEMENTS_FILE = "data/achievements.json"
PROGRESS_FILE = "data/progress.json"
LOG_FILE = "logs/app.log"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger(__name__)


def show_games_list(
    games: list[Game],
    achievements: list[Achievement],
) -> None:
    """Вывести игры и количество достижений в каждой."""
    print("\n--- Список игр в каталоге ---")
    if not games:
        print("Игры еще не добавлены.")
        return
    for game in games:
        count = len(get_achievements_by_game(achievements, game))
        print(f"{game} (Достижений: {count})")


def show_achievements_for_game(
    games: list[Game],
    achievements: list[Achievement],
) -> None:
    """Выбрать игру и вывести ее достижения."""
    if not games:
        print("В каталоге пока нет игр.")
        return
    show_games_list(games, achievements)
    game_id = input_int("\nВведите ID игры: ")
    game = get_game_by_id(games, game_id)
    if game is None:
        print("Игра с указанным ID не найдена.")
        return
    game_achievements = get_achievements_by_game(achievements, game)
    print(f"\n--- Достижения игры: {game.title} ---")
    if not game_achievements:
        print("У этой игры пока нет достижений.")
        return
    for achievement in game_achievements:
        print(achievement)


def show_all_achievements(achievements: list[Achievement]) -> None:
    """Вывести все достижения каталога."""
    print("\n--- Общий список всех достижений ---")
    if not achievements:
        print("Список достижений пуст.")
        return
    for achievement in achievements:
        print(achievement)


def create_progress_card(
    user: User,
    achievement: Achievement,
    progress_list: list[Progress],
) -> str:
    """Создать карточку прогресса, включая еще не начатый прогресс."""
    progress = get_user_progress(progress_list, user, achievement)
    if progress is None:
        progress = Progress(
            id=0,
            user=user,
            achievement=achievement,
            completed_actions=0,
            record_date=str(date.today()),
        )
    return format_achievement_summary(progress)


def add_achievement_from_menu(
    games: list[Game],
    achievements: list[Achievement],
) -> None:
    """Обработать добавление достижения из меню."""
    if not games:
        print("Сначала добавьте хотя бы одну игру (пункт 4).")
        return
    show_games_list(games, achievements)
    game = get_game_by_id(games, input_int("Введите ID игры: "))
    if game is None:
        print("Игры с таким ID не существует.")
        return
    name = input("Название ачивки: ").strip()
    required_actions = input_int("Сколько действий требуется: ")
    is_secret = input("Секретное? (y/n): ").strip().lower() == "y"
    add_achievement(
        achievements,
        game,
        name,
        required_actions,
        is_secret,
    )
    print("Достижение добавлено!")


def record_progress_from_menu(
    users: list[User],
    achievements: list[Achievement],
    progress_list: list[Progress],
) -> None:
    """Обработать запись прогресса из меню."""
    username = input("Имя пользователя: ").strip()
    user = get_user_by_username(users, username)
    if user is None:
        user = add_user(users, username)
        print(f"Создан игрок '{username}' (ID: {user.id})")
    achievement_id = input_int("Введите ID достижения: ")
    achievement = get_achievement_by_id(achievements, achievement_id)
    if achievement is None:
        print("Достижение с таким ID не найдено.")
        return
    completed_actions = input_int("Выполнено действий: ")
    record_date = input_date("Дата (ГГГГ-ММ-ДД): ")
    record_progress(
        progress_list,
        user,
        achievement,
        completed_actions,
        record_date,
    )
    print("Прогресс зафиксирован.")


def show_progress_card_from_menu(
    users: list[User],
    achievements: list[Achievement],
    progress_list: list[Progress],
) -> None:
    """Обработать вывод карточки прогресса из меню."""
    user_input = input("Имя или ID пользователя: ").strip()
    if user_input.isdigit():
        user = get_user_by_id(users, int(user_input))
    else:
        user = get_user_by_username(users, user_input)
    if user is None:
        print("Пользователь не найден.")
        return
    achievement_id = input_int("Введите ID достижения: ")
    achievement = get_achievement_by_id(achievements, achievement_id)
    if achievement is None:
        print("Достижение не найдено.")
        return
    print(f"\n{create_progress_card(user, achievement, progress_list)}")


def main() -> None:
    """Запустить консольное меню трекера достижений."""
    logger.info("Запуск приложения")
    games = load_games(GAMES_FILE)
    users = load_users(USERS_FILE)
    achievements = load_achievements(ACHIEVEMENTS_FILE, games)
    progress_list = load_progress(PROGRESS_FILE, users, achievements)

    while True:
        print("\n=== Game Achievement Tracker ===")
        print("1. Показать список игр")
        print("2. Показать достижения выбранной игры")
        print("3. Показать все достижения")
        print("4. Добавить игру")
        print("5. Добавить достижение к игре")
        print("6. Найти достижение")
        print("7. Показать всех игроков")
        print("8. Зафиксировать прогресс игрока")
        print("9. Показать карточку прогресса")
        print("0. Сохранить и выйти")

        choice = input("Выберите пункт меню: ").strip()
        if choice == "1":
            show_games_list(games, achievements)
        elif choice == "2":
            show_achievements_for_game(games, achievements)
        elif choice == "3":
            show_all_achievements(achievements)
        elif choice == "4":
            title = input("Название игры: ").strip()
            if title:
                game = add_game(games, title)
                print(f"Игра '{game.title}' добавлена (ID: {game.id})")
            else:
                print("Название не может быть пустым.")
        elif choice == "5":
            add_achievement_from_menu(games, achievements)
        elif choice == "6":
            query = input("Введите название или ID достижения: ").strip()
            if query.isdigit():
                achievement = get_achievement_by_id(achievements, int(query))
                results = [] if achievement is None else [achievement]
            else:
                results = list(find_achievements(achievements, query))
            show_all_achievements(results)
        elif choice == "7":
            show_users(users)
        elif choice == "8":
            record_progress_from_menu(users, achievements, progress_list)
        elif choice == "9":
            show_progress_card_from_menu(users, achievements, progress_list)
        elif choice == "0":
            save_games(GAMES_FILE, games)
            save_users(USERS_FILE, users)
            save_achievements(ACHIEVEMENTS_FILE, achievements)
            save_progress(PROGRESS_FILE, progress_list)
            logger.info("Данные сохранены, приложение завершено")
            break
        else:
            print("Неизвестный пункт меню.")
            logger.warning("Неизвестный пункт меню: %s", choice)


if __name__ == "__main__":
    main()
