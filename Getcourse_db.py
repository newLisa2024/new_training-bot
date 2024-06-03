import sqlite3


def init_getcourse_database():
    conn = sqlite3.connect('getcourse.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS getcourse_users (
            user_id INTEGER PRIMARY KEY,
            is_active INTEGER DEFAULT 1
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parameters (
            param_id INTEGER PRIMARY KEY AUTOINCREMENT,
            param_text TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    ''')

    conn.commit()
    conn.close()

    @error_handler
    @bot.message_handler(commands=['start'])
    def start(message):
        user_id = message.from_user.id
        print(user_id)
        # try:
        #    user_status = tdb.is_user_in_db(user_id)
        # проверяем, если ли пользователь в нашей базе данных,
        # если есть, но неактивный (is_active = 0), он имеет доступ к тренажеру в разделе статистики
        # если есть и активный, ему доступны все функции
        #    if user_status is not None:
        #       bot.send_message(message.chat.id, start_message)
        #        keyboard = create_inline_keyboard(['test_mode', 'statistics'])
        #        bot.send_message(message.chat.id, start_message, reply_markup=keyboard)
        #        return
        # except Exception as e:
        #    bot.send_message(message.chat.id, f"Произошла ошибка при проверке пользователя: {e}")
        #   return

        # если нет ссылки с параметром, а просто нажимаем /start
        try:
            param_text = message.text.split()[1]
        except IndexError:
            bot.reply_to(message, "Для авторизации в тренажере нужно перейти по ссылке от университета ZeroCoder")
            return

        # если параметр существует, но его нет в нашем списке
        # if not gc.check_parameter(param_text):
        #    bot.reply_to(message, "У Вас нет доступа к тренажеру. Пожалуйста, обратитесь к куратору.")
        #    return
        # если параметр существует и активен, но пользователя нет в активных студентах
        # if not gc.check_user(user_id):
        #    bot.reply_to(message, "У Вас нет доступа к тренажеру. Пожалуйста, обратитесь к куратору.")
        #    return

        # здесь будет функция добавления пользователя в базу бота
        # def add_user(user_id, user_name):

        # Отправка приветственного сообщения с клавиатурой
        keyboard = create_inline_keyboard(['test_mode', 'statistics'])
        bot.send_message(message.chat.id, start_message, reply_markup=keyboard)



