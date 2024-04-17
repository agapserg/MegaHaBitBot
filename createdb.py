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

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
