import telebot
from datetime import datetime
import time
from config import BOT_TOKEN, params
from GetCourse_Backend import *
from db import *
from Frontend import *
from Backend import *
from transparent_user_graph import *
import logging

# Вызов функции для создания базы данных и таблиц
#init_database()


bot = telebot.TeleBot(BOT_TOKEN)
print("bot has started", datetime.now())



tdb = Training_db()


#запустить один раз, меняет темы вопросов с Нет на Микс
#tdb.change_question_topics()

#получаем список всех тем
list_of_topics = tdb.get_all_topics()
print(list_of_topics)

# Настройка логирования
logging.basicConfig(level=logging.ERROR, filename='bot_errors.log', filemode='a',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}", exc_info=True)
            message = kwargs.get('message') or args[0]
            keyboard = create_inline_keyboard(['test_mode', 'statistics'])
            bot.send_message(message.chat.id, "Произошла ошибка.", reply_markup=keyboard)
    return wrapper
@error_handler
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    print(user_id)

     #если нет ссылки с параметром, а просто нажимаем /start
    try:
        param_text = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Для авторизации в тренажере нужно перейти по ссылке от университета ZeroCoder")
        return


    #если параметр введен, но его нет в нашем списке
    if param_text not in params:
        bot.reply_to(message, "Эта ссылка не поддерживается. Обратитесь к куратору.")
        return

    #добавляем пользователя в базу данных
    tdb.add_user(user_id)

    # Отправка приветственного сообщения с клавиатурой
    keyboard = create_inline_keyboard(['test_mode', 'statistics'])
    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'test_mode')
@error_handler
def handle_test_mode(call):
    user_id = call.from_user.id
    try:
        user_status = tdb.is_user_in_db(user_id)
        # проверяем, если пользователь неактивный (is_active = 0),
        # он имеет доступ к тренажеру только в разделе статистики
        # отказываем в доступе к Тестированию
        if user_status == 0:
            keyboard = create_inline_keyboard(['menu'])
            bot.send_message(call.message.chat.id, 'У Вас нет доступа к Тестированию. Пожалуйста, обратитесь к куратору.', reply_markup=keyboard)
            return
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка при проверке пользователя: {e}")
        return

    keyboard = create_inline_keyboard(['all_questions', 'choose_topic', 'menu'])
    bot.send_message(call.message.chat.id, "Давайте начнём! Выберите один из вариантов:\n"
                                      "1. Ответить на все вопросы\n"
                                      "2. Выбрать конкретную тему", reply_markup=keyboard)
    # Здесь можно добавить логику для запуска тестирования

# Обработка кнопки "Статистика"
@bot.callback_query_handler(func=lambda call: call.data == 'statistics')
@error_handler
def handle_statistics(call):
    keyboard=create_inline_keyboard(['text_report', 'graph_report', 'menu'])
    bot.send_message(call.message.chat.id, "Какой отчет Вы хотите посмотреть?", reply_markup=keyboard)
    # Здесь можно добавить логику для показа статистики


@bot.callback_query_handler(func=lambda call: call.data == 'menu')
@error_handler
def handle_menu(call):
    keyboard=create_inline_keyboard(['test_mode', 'statistics'])
    bot.send_message(call.message.chat.id, "Выберите раздел", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'all_questions')
@error_handler
def handle_all_questions(call):
    #здесь будет функция, которая будет считать, на сколько вопросов вообще из всех уже ответил пользователь
    #если ни на сколько, то она будет сразу посылать вопрос
    #если ответилл на сколько-то, пишем Вы уже ответили на 3 вопроса из 1096. Продолжим!
    bot.send_message(call.message.chat.id, 'Тут будет сказано: Вы уже ответили на 3 вопроса из 1096. Продолжим!')
    bot.send_message(call.message.chat.id, timer_message)
    #здесь будет вызываться таймер
    bot.send_message(call.message.chat.id, 'Тут будет таймер')
    #здесь будет функция, которая отправляет вопрос
    keyboard = create_inline_keyboard(['skip_question', 'menu'])
    bot.send_message(call.message.chat.id, 'Тут будет вопрос', reply_markup=keyboard)
    #Продумать, как принимать от пользователя ввод с клавиатуры


# Обработчик кнопки 'choose_topic'
@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_topic'))
@error_handler
def choose_topic(call):
    global list_of_topics

    if not list_of_topics:
        bot.send_message(call.message.chat.id, "Темы не найдены.")
        return

    _, page = call.data.split(':') if ':' in call.data else ('choose_topic', '0')
    page = int(page)

    topics_per_page = 8
    start = page * topics_per_page
    end = start + topics_per_page
    topics = list_of_topics[start:end]

    # Создаем список кнопок с темами
    button_keys = [f'topic_{i}' for i in range(start, end) if i < len(list_of_topics)]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=topics[i - start], callback_data=button_keys[i - start]) for i in range(start, end) if i < len(list_of_topics)]
    keyboard.add(*buttons)

    # Добавляем кнопки для навигации
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton(text=buttons_dict['left'], callback_data=f'choose_topic:{page-1}'))
    if end < len(list_of_topics):
        nav_buttons.append(types.InlineKeyboardButton(text=buttons_dict['right'], callback_data=f'choose_topic:{page+1}'))

    if nav_buttons:
        keyboard.add(*nav_buttons)

    keyboard.add(types.InlineKeyboardButton(text=buttons_dict['menu'], callback_data='menu'))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите тему:', reply_markup=keyboard)


# Обработчик для выбора конкретной темы (пример)

# Обработчик кнопки выбора темы
@bot.callback_query_handler(func=lambda call: call.data.startswith('topic_'))
def topic_selected(call):
    try:
        topic_index = int(call.data.split('_')[1])  # Извлекаем индекс выбранной темы
        topic_name = list_of_topics[topic_index]    # Получаем название темы по индексу

        # Получаем количество правильно отвеченных вопросов и общее количество вопросов по данной теме
        correct_answers_count, total_questions_count = tdb.get_correct_answers_count(call.from_user.id, topic_name)

        # Создаем прогресс-бар
        filename = draw_progress_bar(call.from_user.id, correct_answers_count, total_questions_count, topic_name)

        # Отправляем сообщение с выбранной темой и прогресс-баром
        bot.send_message(call.message.chat.id, f'Вы выбрали тему: "{topic_name}"\nВаш прогресс:')
        with open(filename, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)

        # Удаляем файл после отправки
        os.remove(filename)

    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')
# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)