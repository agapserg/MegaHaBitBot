import sqlite3

def process_and_insert_data(file_path):
    # Подключаемся к базе данных
    conn = sqlite3.connect('MegaHaBitBot.db')
    c = conn.cursor()

    # Открываем и читаем файл
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Разделяем строку по запятым и удаляем пробелы в начале и конце
            parts = line.strip().split(', ')
            if len(parts) == 4:  # Убедимся, что у нас есть четыре части
                name, veg_frut, group, color = parts
                
                # Вставляем данные в таблицу
                c.execute('''
                    INSERT INTO c_veg_frut (name, veg_frut, grp, clr) 
                    VALUES (?, ?, ?, ?)
                ''', (name, veg_frut, group, color))

    # Фиксируем изменения и закрываем соединение
    conn.commit()
    conn.close()

# Вызываем функцию с путём к файлу данных
file_path = 'veg_frut.txt'
process_and_insert_data(file_path)
