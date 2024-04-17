from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
import sqlite3
from config import API_TOKEN  # Импортируем токен из файла config.py
import datetime as dt
from collections import defaultdict


# Создание экземпляра бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Путь к файлу базы данных
DATABASE_PATH = 'MegaHaBitBot.db'

conn = sqlite3.connect(DATABASE_PATH)
c = conn.cursor()

# Словарь для очков по символам
emoji_points = {
    "🟩": 20,
    "🟨": 15,
    "🟧": 10,
    "🟥": 7,
    "🟫": 5,
    "⬛️": 4,
    "🟪": 3,
    "🟦": 2,
    "⬜️": 1
}


# Функция для записи/обновления данных пользователя в таблице a_users
def add_user_to_db(user_id, first_name, last_name, tg_nick):
    c.execute("SELECT * FROM a_users WHERE tg_user_id=?", (user_id,))
    existing_user = c.fetchone()
    if existing_user:
        c.execute("UPDATE a_users SET tg_firstname=?, tg_lastname=?, tg_nick=? WHERE tg_user_id=?", (first_name, last_name, tg_nick, user_id))
    else:
        c.execute("INSERT INTO a_users (tg_user_id, tg_firstname, tg_lastname, tg_nick) VALUES (?, ?, ?, ?)", (user_id, first_name, last_name, tg_nick))
    conn.commit()

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    tg_nick = message.from_user.username

    add_user_to_db(user_id, first_name, last_name, tg_nick)

    # Отправляем приветственное сообщение и инлайн-меню
    keyboard = types.InlineKeyboardMarkup()
    buttons = [
        types.InlineKeyboardButton(text="Сон", callback_data="sleep"),
        types.InlineKeyboardButton(text="Овощи", callback_data="vegetables"),
        types.InlineKeyboardButton(text="Алкоголь", callback_data="alcohol"),
        types.InlineKeyboardButton(text="Курение", callback_data="smoking"),
        types.InlineKeyboardButton(text="Физкультура", callback_data="exercise"),
    ]
    for button in buttons:
        keyboard.add(button)  # Добавляем каждую кнопку на отдельной строке
    welcome_text = "Поздравляю с успешной регистрацией в MegaHaBitBot'е, теперь можно выбрать активности."
    await message.reply(welcome_text, reply_markup=keyboard)

# Обработчик выбора "Сон"
@dp.callback_query_handler(lambda c: c.data == 'sleep')
async def handle_sleep(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    time_buttons = [
        types.InlineKeyboardButton("🟩(22-23)", callback_data="22-23"),
        types.InlineKeyboardButton("🟨(23-00)", callback_data="23-00"),
        types.InlineKeyboardButton("🟧(00-01)", callback_data="00-01"),
        types.InlineKeyboardButton("🟥(01-02)", callback_data="01-02"),
        types.InlineKeyboardButton("🟫(02-03)", callback_data="02-03"),
        types.InlineKeyboardButton("⬛️(04-05)", callback_data="04-05"),
        types.InlineKeyboardButton("🟪(06-07)", callback_data="06-07"),
        types.InlineKeyboardButton("🟦(07-08)", callback_data="07-08"),
        types.InlineKeyboardButton("⬜️(09-10)", callback_data="09-10"),
    ]
    for button in time_buttons:
        keyboard.add(button)  # Добавляем каждую кнопку на отдельной строке
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите время сна:", reply_markup=keyboard)

def update_or_insert_sleep_data(user_id, sleep_emoji):
    today_date = dt.datetime.now().strftime('%Y-%m-%d')
    
    # Проверяем, есть ли уже запись на текущую дату для этого пользователя
    c.execute("SELECT * FROM b_stats WHERE date=? AND tg_user_id=?", (today_date, user_id))
    existing_record = c.fetchone()
    
    if existing_record:
        # Если запись найдена, обновляем значение sleep
        c.execute("UPDATE b_stats SET sleep=? WHERE date=? AND tg_user_id=?", (sleep_emoji, today_date, user_id))
    else:
        # Если запись не найдена, добавляем новую
        c.execute("INSERT INTO b_stats (date, tg_user_id, sleep) VALUES (?, ?, ?)", (today_date, user_id, sleep_emoji))
    
    conn.commit()

# Обработчик нажатия на временные кнопки сна
@dp.callback_query_handler(lambda c: c.data in ["22-23", "23-00", "00-01", "01-02", "02-03", "04-05", "06-07", "07-08", "09-10"])
async def handle_sleep_time(callback_query: types.CallbackQuery):
    sleep_emoji_mapping = {
        "22-23": "🟩",
        "23-00": "🟨",
        "00-01": "🟧",
        "01-02": "🟥",
        "02-03": "🟫",
        "04-05": "⬛️",
        "06-07": "🟪",
        "07-08": "🟦",
        "09-10": "⬜️",
    }
    user_id = callback_query.from_user.id
    sleep_emoji = sleep_emoji_mapping[callback_query.data]
    update_or_insert_sleep_data(user_id, sleep_emoji)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Время сна {sleep_emoji} записано.")

def update_or_insert_vegetable_data(user_id, vegetable_emoji):
    today_date = dt.datetime.now().strftime('%Y-%m-%d')
    
    c.execute("SELECT * FROM b_stats WHERE date=? AND tg_user_id=?", (today_date, user_id))
    existing_record = c.fetchone()
    
    if existing_record:
        c.execute("UPDATE b_stats SET veg=? WHERE date=? AND tg_user_id=?", (vegetable_emoji, today_date, user_id))
    else:
        c.execute("INSERT INTO b_stats (date, tg_user_id, veg) VALUES (?, ?, ?)", (today_date, user_id, vegetable_emoji))
    
    conn.commit()

# Обработчик выбора "Овощи"
@dp.callback_query_handler(lambda c: c.data == 'vegetables')
async def handle_vegetables(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    veg_buttons = [
        types.InlineKeyboardButton("🟩(5+ овощей)", callback_data="5+"),
        types.InlineKeyboardButton("🟨(4 овоща)", callback_data="4"),
        types.InlineKeyboardButton("🟧(3 овоща)", callback_data="3"),
        types.InlineKeyboardButton("🟥(2 овоща)", callback_data="2"),
        types.InlineKeyboardButton("🟫(1 овощ)", callback_data="1"),
    ]
    for button in veg_buttons:
        keyboard.add(button)  # Добавляем каждую кнопку на отдельной строке
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите количество употребляемых овощей:", reply_markup=keyboard)

# Обработчик нажатия на кнопки количества овощей
@dp.callback_query_handler(lambda c: c.data in ["5+", "4", "3", "2", "1"])
async def handle_vegetable_count(callback_query: types.CallbackQuery):
    veg_emoji_mapping = {
        "5+": "🟩",
        "4": "🟨",
        "3": "🟧",
        "2": "🟥",
        "1": "🟫",
    }
    user_id = callback_query.from_user.id
    vegetable_emoji = veg_emoji_mapping[callback_query.data]
    update_or_insert_vegetable_data(user_id, vegetable_emoji)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Количество овощей {vegetable_emoji} записано.")

def update_or_insert_alcohol_data(user_id, alcohol_emoji):
    today_date = dt.datetime.now().strftime('%Y-%m-%d')
    
    c.execute("SELECT * FROM b_stats WHERE date=? AND tg_user_id=?", (today_date, user_id))
    existing_record = c.fetchone()
    
    if existing_record:
        c.execute("UPDATE b_stats SET alco=? WHERE date=? AND tg_user_id=?", (alcohol_emoji, today_date, user_id))
    else:
        c.execute("INSERT INTO b_stats (date, tg_user_id, alco) VALUES (?, ?, ?)", (today_date, user_id, alcohol_emoji))
    
    conn.commit()

# Обработчик выбора "Алкоголь"
@dp.callback_query_handler(lambda c: c.data == 'alcohol')
async def handle_alcohol(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    alcohol_buttons = [
        types.InlineKeyboardButton("🟩(не пил)", callback_data="none"),
        types.InlineKeyboardButton("🟨(1 банка пива)", callback_data="1beer"),
        types.InlineKeyboardButton("🟧(3 банки пива)", callback_data="3beer"),
        types.InlineKeyboardButton("🟥(1 рюмка)", callback_data="1shot"),
        types.InlineKeyboardButton("🟫(3 рюмки)", callback_data="3shots"),
        types.InlineKeyboardButton("⬛️(1 бутыль)", callback_data="1bottle"),
    ]
    for button in alcohol_buttons:
        keyboard.add(button)  # Добавляем каждую кнопку на отдельной строке
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите количество употребляемого алкоголя:", reply_markup=keyboard)

# Обработчик нажатия на кнопки количества алкоголя
@dp.callback_query_handler(lambda c: c.data in ["none", "1beer", "3beer", "1shot", "3shots", "1bottle"])
async def handle_alcohol_amount(callback_query: types.CallbackQuery):
    alcohol_emoji_mapping = {
        "none": "🟩",
        "1beer": "🟨",
        "3beer": "🟧",
        "1shot": "🟥",
        "3shots": "🟫",
        "1bottle": "⬛️",
    }
    user_id = callback_query.from_user.id
    alcohol_emoji = alcohol_emoji_mapping[callback_query.data]
    update_or_insert_alcohol_data(user_id, alcohol_emoji)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Количество употребляемого алкоголя {alcohol_emoji} записано.")

def update_or_insert_smoking_data(user_id, smoking_emoji):
    today_date = dt.datetime.now().strftime('%Y-%m-%d')
    
    c.execute("SELECT * FROM b_stats WHERE date=? AND tg_user_id=?", (today_date, user_id))
    existing_record = c.fetchone()
    
    if existing_record:
        c.execute("UPDATE b_stats SET smok=? WHERE date=? AND tg_user_id=?", (smoking_emoji, today_date, user_id))
    else:
        c.execute("INSERT INTO b_stats (date, tg_user_id, smok) VALUES (?, ?, ?)", (today_date, user_id, smoking_emoji))
    
    conn.commit()

# Обработчик выбора "Курение"
@dp.callback_query_handler(lambda c: c.data == 'smoking')
async def handle_smoking(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    smoking_buttons = [
        types.InlineKeyboardButton("🟩(не курил)", callback_data="no_smoking"),
        types.InlineKeyboardButton("🟨(читал Аллена Карра)", callback_data="read_carr"),
    ]
    for button in smoking_buttons:
        keyboard.add(button)  # Добавляем каждую кнопку на отдельной строке
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите ваш статус курения за сегодня:", reply_markup=keyboard)

# Обработчик нажатия на кнопки статуса курения
@dp.callback_query_handler(lambda c: c.data in ["no_smoking", "read_carr"])
async def handle_smoking_status(callback_query: types.CallbackQuery):
    smoking_emoji_mapping = {
        "no_smoking": "🟩",
        "read_carr": "🟨",
    }
    user_id = callback_query.from_user.id
    smoking_emoji = smoking_emoji_mapping[callback_query.data]
    update_or_insert_smoking_data(user_id, smoking_emoji)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Статус курения {smoking_emoji} зафиксирован.")

def update_or_insert_fitness_data(user_id, fitness_emoji):
        today_date = dt.datetime.now().strftime('%Y-%m-%d')
        
        c.execute("SELECT * FROM b_stats WHERE date=? AND tg_user_id=?", (today_date, user_id))
        existing_record = c.fetchone()
        
        if existing_record:
            c.execute("UPDATE b_stats SET fit=? WHERE date=? AND tg_user_id=?", (fitness_emoji, today_date, user_id))
        else:
            c.execute("INSERT INTO b_stats (date, tg_user_id, fit) VALUES (?, ?, ?)", (today_date, user_id, fitness_emoji))
        conn.commit()

# Обработчик выбора "Физкультура"
@dp.callback_query_handler(lambda c: c.data == 'exercise')
async def handle_exercise(callback_query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup()
    exercise_buttons = [
        types.InlineKeyboardButton("🟩(2+ часа в фитнесе)", callback_data="2h+"),
        types.InlineKeyboardButton("🟨(1+ час в фитнесе)", callback_data="1h+"),
        types.InlineKeyboardButton("🟧(30+ мин любая активность)", callback_data="30min+"),
        types.InlineKeyboardButton("🟥(15+ мин любая активность)", callback_data="15min+"),
        types.InlineKeyboardButton("🟫(5+ мин любая активность)", callback_data="5min+"),
        types.InlineKeyboardButton("⬛️(встал размялся)", callback_data="stretched"),
    ]
    for button in exercise_buttons:
        keyboard.add(button)
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, "Выберите уровень вашей физической активности:", reply_markup=keyboard)

# Обработчик нажатия на кнопки физической активности
@dp.callback_query_handler(lambda c: c.data in ["2h+", "1h+", "30min+", "15min+", "5min+", "stretched"])
async def handle_fitness_level(callback_query: types.CallbackQuery):
    fitness_emoji_mapping = {
        "2h+": "🟩",
        "1h+": "🟨",
        "30min+": "🟧",
        "15min+": "🟥",
        "5min+": "🟫",
        "stretched": "⬛️",
    }
    user_id = callback_query.from_user.id
    fitness_emoji = fitness_emoji_mapping[callback_query.data]
    update_or_insert_fitness_data(user_id, fitness_emoji)
    
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Уровень физической активности {fitness_emoji} зафиксирован.")

# Хендлер для команды /toptop
@dp.message_handler(commands=['toptop'])
async def handle_toptop(message: types.Message):
    top_scores = calculate_top_scores()
    result_message = "🏆 Top Users by Activity Points:\n\n"
    for rank, (user_id, points) in enumerate(top_scores, start=1):
        result_message += f"{rank}. User {user_id}: {points} points\n"
    await message.reply(result_message)

# Функция для подсчета очков и формирования списка топ пользователей
def calculate_top_scores():
    with sqlite3.connect(DATABASE_PATH) as conn:
        c = conn.cursor()
        # Получаем все записи из таблицы b_stats
        c.execute("SELECT tg_user_id, sleep, veg, alco, smok, fit FROM b_stats")
        user_scores = defaultdict(int)
        
        # Подсчитываем очки для каждого пользователя
        for row in c.fetchall():
            user_id = row[0]
            for activity in row[1:]:
                if activity and activity in emoji_points:
                    user_scores[user_id] += emoji_points[activity]
        
        # Сортируем пользователей по количеству очков в убывающем порядке
        sorted_scores = sorted(user_scores.items(), key=lambda item: item[1], reverse=True)
        # Возвращаем топ пользователей
        return sorted_scores[:10]  # Ограничиваем топ 10 пользователями

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
