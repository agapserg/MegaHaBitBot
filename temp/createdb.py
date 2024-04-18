import sqlite3

def create_database():
    # Подключение к базе данных (если файла не существует, он будет создан)
    conn = sqlite3.connect('MegaHaBitBot.db')
    c = conn.cursor()

    # Создание таблицы users
    c.execute('''CREATE TABLE IF NOT EXISTS a_users (
                int_nick TEXT,
                tg_user_id TEXT UNIQUE,
                tg_nick TEXT,
                tg_firstname TEXT,
                tg_lastname TEXT
                )''')

    # Создание таблицы stats
    c.execute('''CREATE TABLE IF NOT EXISTS b_stats (
                date TEXT,
                tg_user_id TEXT,
                sleep TEXT,
                veg TEXT,
                alco TEXT,
                smok TEXT,
                fit TEXT
                )''')

    # Проверка и добавление столбца name_frut если он отсутствует
    c.execute("PRAGMA table_info(b_stats)")
    columns = [info[1] for info in c.fetchall()]
    if "name_veg" not in columns:
        c.execute("ALTER TABLE b_stats ADD COLUMN name_veg TEXT")

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
