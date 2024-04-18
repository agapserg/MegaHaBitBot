import sqlite3

def create_table():
    # Подключаемся к базе данных (или создаем новую, если она не существует)
    conn = sqlite3.connect('MegaHaBitBot.db')
    c = conn.cursor()

    # Создаем таблицу c_veg_frut, если она не существует
    c.execute('''
        CREATE TABLE IF NOT EXISTS c_veg_frut (
            name TEXT,
            veg_frut TEXT,
            grp TEXT,
            clr TEXT
        )
    ''')

    # Фиксируем изменения и закрываем соединение
    conn.commit()
    conn.close()

# Вызываем функцию для создания таблицы
create_table()
