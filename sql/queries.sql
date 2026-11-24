-- 1. Список игр
SELECT id, title
FROM games
ORDER BY title;

-- 2. Список достижений
SELECT id, name, required_actions, is_secret, game_id
FROM achievements
ORDER BY name;

-- 3. Фильтр достижений по числу действий
SELECT id, name, required_actions
FROM achievements
WHERE required_actions >= 50
ORDER BY required_actions;

-- 4. Секретные достижения
SELECT id, name
FROM achievements
WHERE is_secret = 1;

-- 5. Достижения вместе с игрой
SELECT
    achievements.id,
    achievements.name,
    games.title AS game_title
FROM achievements
JOIN games ON games.id = achievements.game_id
ORDER BY games.title, achievements.name;

-- 6. Записи прогресса со связанными объектами
SELECT
    progress.id,
    users.username,
    achievements.name AS achievement_name,
    games.title AS game_title,
    progress.completed_actions,
    progress.record_date
FROM progress
JOIN users ON users.id = progress.user_id
JOIN achievements ON achievements.id = progress.achievement_id
JOIN games ON games.id = achievements.game_id
ORDER BY progress.record_date DESC;

-- 7. Прогресс в процессе
SELECT progress.id, users.username, achievements.name
FROM progress
JOIN users ON users.id = progress.user_id
JOIN achievements ON achievements.id = progress.achievement_id
WHERE progress.completed_actions > 0
  AND progress.completed_actions < achievements.required_actions;

-- 8. Полная карточка одной записи прогресса
SELECT
    progress.id,
    users.username,
    achievements.name AS achievement_name,
    games.title AS game_title
FROM progress
JOIN users ON users.id = progress.user_id
JOIN achievements ON achievements.id = progress.achievement_id
JOIN games ON games.id = achievements.game_id
WHERE progress.id = 1;

-- 9. Достижения, не полученные на выбранную дату
SELECT achievements.id, achievements.name, games.title
FROM achievements
JOIN games ON games.id = achievements.game_id
WHERE NOT EXISTS (
    SELECT 1
    FROM progress
    WHERE progress.achievement_id = achievements.id
      AND progress.completed_actions >= achievements.required_actions
      AND progress.record_date <= '2026-10-01'
)
ORDER BY games.title, achievements.name;

-- 10. Количество записей прогресса
SELECT COUNT(id) AS progress_count
FROM progress;

-- 11. Количество достижений
SELECT COUNT(id) AS achievements_count
FROM achievements;

-- 12. Количество записей прогресса по играм
SELECT
    games.title AS game_title,
    COUNT(progress.id) AS progress_count
FROM games
LEFT JOIN achievements ON achievements.game_id = games.id
LEFT JOIN progress ON progress.achievement_id = achievements.id
GROUP BY games.id, games.title
ORDER BY progress_count DESC, games.title;

-- 13. Количество полученных достижений по игрокам
SELECT
    users.username,
    COUNT(progress.id) AS obtained_count
FROM users
LEFT JOIN progress ON progress.user_id = users.id
LEFT JOIN achievements ON achievements.id = progress.achievement_id
    AND progress.completed_actions >= achievements.required_actions
GROUP BY users.id, users.username
ORDER BY obtained_count DESC;

-- 14. Игры, у которых записей прогресса больше нуля
SELECT games.title, COUNT(progress.id) AS progress_count
FROM games
JOIN achievements ON achievements.game_id = games.id
JOIN progress ON progress.achievement_id = achievements.id
GROUP BY games.id, games.title
HAVING COUNT(progress.id) > 0
ORDER BY progress_count DESC;
