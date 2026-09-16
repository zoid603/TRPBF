from datetime import date
from storage import load_json, save_json
from utils import input_int, input_date
from users import add_user, get_user_by_username
from games import add_game, get_game_by_id
from achievements import (
    add_achievement,
    find_achievements,
    sort_achievements_by_complexity,
    get_achievement_by_id,
    get_achievements_by_game,
)
from progress import (
    calculate_progress_percent,
    check_unlock_status,
    format_achievement_summary,
    record_progress,
    get_user_progress,
)

USERS_FILE = "data/users.json"
GAMES_FILE = "data/games.json"
ACHIEVEMENTS_FILE = "data/achievements.json"
PROGRESS_FILE = "data/progress.json"


def show_games_list(games, achievements):
    """Вывод всех зарегистрированных игр и количества ачивок в них."""
    print("\n--- Список игр в каталоге ---")
    if not games:
        print("Игры еще не добавлены.")
        return
    for g in games:
        count = len(get_achievements_by_game(achievements, g["id"]))
        print(f"ID {g['id']}: {g['title']} (Достижений: {count})")


def show_achievements_for_game(games, achievements):
    """Выбор игры и отображение только её достижений."""
    if not games:
        print("В каталоге пока нет игр.")
        return
    show_games_list(games, achievements)
    game_id = input_int("\nВведите ID игры: ")
    game = get_game_by_id(games, game_id)
    if not game:
        print("Игра с указанным ID не найдена.")
        return

    game_achs = get_achievements_by_game(achievements, game_id)
    print(f"\n--- Достижения игры: {game['title']} ---")
    if not game_achs:
        print("У этой игры пока нет достижений.")
        return

    for a in game_achs:
        sec = " [Секретное]" if a.get("is_secret") else ""
        req = a['required_actions']
        print(f"  • ID {a['id']}: {a['name']} — нужно: {req}{sec}")


def show_all_achievements(achievements, games):
    """Вывод абсолютно всех ачивок базы."""
    print("\n--- Общий список всех достижений ---")
    if not achievements:
        print("Список достижений пуст.")
        return
    for a in achievements:
        game = get_game_by_id(games, a.get("game_id", 0))
        game_title = game["title"] if game else "Неизвестно"
        sec = " [Секретное]" if a.get("is_secret") else ""
        req = a['required_actions']
        info = f"ID {a['id']}: [{game_title}] {a['name']} (Требуется: {req})"
        print(f"{info}{sec}")


def main() -> None:
    users = load_json(USERS_FILE)
    games = load_json(GAMES_FILE)
    achievements = load_json(ACHIEVEMENTS_FILE)
    progress_list = load_json(PROGRESS_FILE)

    while True:
        print("\n=== Game Achievement Tracker ===")
        print("1. Показать список игр")
        print("2. Показать достижения конкретной игры")
        print("3. Показать вообще все достижения")
        print("4. Добавить игру")
        print("5. Добавить достижение к игре")
        print("6. Найти достижения по названию")
        print("7. Отсортировать достижения по сложности")
        print("8. Зафиксировать прогресс игрока")
        print("9. Показать карточку прогресса (сценарий ПР1)")
        print("0. Сохранить и выйти")

        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            show_games_list(games, achievements)

        elif choice == "2":
            show_achievements_for_game(games, achievements)

        elif choice == "3":
            show_all_achievements(achievements, games)

        elif choice == "4":
            title = input("Название игры: ").strip()
            if not title:
                print("Название не может быть пустым.")
                continue
            g = add_game(games, title)
            print(f"Игра '{g['title']}' добавлена (ID: {g['id']})")

        elif choice == "5":
            if not games:
                print("Сначала добавьте хотя бы одну игру (пункт 4).")
                continue
            show_games_list(games, achievements)
            game_id = input_int("Введите ID игры для добавления ачивки: ")
            if not get_game_by_id(games, game_id):
                print("Игры с таким ID не существует.")
                continue

            name = input("Название ачивки: ").strip()
            req = input_int("Сколько действий требуется для получения: ")
            sec = input("Секретное? (y/n): ").strip().lower() == "y"
            add_achievement(achievements, game_id, name, req, sec)
            print("Достижение добавлено!")

        elif choice == "6":
            query = input("Введите поисковый запрос: ").strip()
            results = list(find_achievements(achievements, query))
            show_all_achievements(results, games)

        elif choice == "7":
            sorted_achs = sort_achievements_by_complexity(achievements)
            show_all_achievements(sorted_achs, games)

        elif choice == "8":
            username = input("Имя пользователя: ").strip()
            user = get_user_by_username(users, username)
            if not user:
                user = add_user(users, username)
                print(f"Создан игрок '{username}' (ID: {user['id']})")

            ach_id = input_int("Введите ID достижения: ")
            ach = get_achievement_by_id(achievements, ach_id)
            if not ach:
                print("Достижение с таким ID не найдено.")
                continue

            completed = input_int("Выполнено действий: ")
            rec_date = input_date("Дата (ГГГГ-ММ-ДД): ")
            record_progress(
                progress_list, user["id"], ach_id, completed, rec_date
            )
            print("Прогресс зафиксирован.")

        elif choice == "9":
            username = input("Имя пользователя: ").strip()
            user = get_user_by_username(users, username)
            if not user:
                print("Пользователь не найден.")
                continue

            ach_id = input_int("Введите ID достижения: ")
            ach = get_achievement_by_id(achievements, ach_id)
            if not ach:
                print("Достижение не найдено.")
                continue

            game = get_game_by_id(games, ach["game_id"])
            game_title = game["title"] if game else "Неизвестная игра"

            prog = get_user_progress(progress_list, user["id"], ach_id)
            completed = prog["completed_actions"] if prog else 0
            rec_date = prog["record_date"] if prog else str(date.today())

            pct = calculate_progress_percent(
                completed, ach["required_actions"]
            )
            status = check_unlock_status(completed, ach["required_actions"])
            card = format_achievement_summary(
                user["username"],
                game_title,
                ach["name"],
                status,
                pct,
                rec_date,
            )
            print(f"\n{card}")

        elif choice == "0":
            save_json(USERS_FILE, users)
            save_json(GAMES_FILE, games)
            save_json(ACHIEVEMENTS_FILE, achievements)
            save_json(PROGRESS_FILE, progress_list)
            print("Все изменения сохранены в JSON. Выход.")
            break
        else:
            print("Неизвестный пункт меню.")


if __name__ == "__main__":
    main()
