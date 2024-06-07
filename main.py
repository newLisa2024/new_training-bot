from statistics_text import *
import pandas as pd
import schedule
import threading
from terminology_short import *
import subprocess
import io
import time
import random
from config import BOT_TOKEN, params, STICKER_CAT, STICKER_SUCCESS, STICKER_HR, LINUX_FFMPEG_PATH
from GetCourse_Backend import *
from Frontend import *
from Backend import *
from WORKING_individual_user_graph import *
import logging
from PIL import Image

# Вызов функции для создания базы данных и таблиц
#init_database()

#УСТАНАВЛИВАЕМ СЕКУНДЫ НА ТАЙМЕР
timer_seconds = 120

bot = telebot.TeleBot(BOT_TOKEN)
print("bot has started", datetime.now())



tdb = Training_db()


#запустить один раз, меняет темы вопросов с Нет на Микс
tdb.change_question_topics()

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
            call = kwargs.get('call') or args[0]
            keyboard = create_inline_keyboard(['test_mode', 'statistics'])
            if isinstance(call, telebot.types.CallbackQuery):
                bot.send_message(call.message.chat.id, "Произошла ошибка.", reply_markup=keyboard)
            else:
                bot.send_message(call.chat.id, "Произошла ошибка.", reply_markup=keyboard)
    return wrapper

#@error_handler
#def create_inline_keyboard(button_keys):
#    keyboard = types.InlineKeyboardMarkup(row_width=2)
#    buttons = [types.InlineKeyboardButton(text=buttons_dict[key], callback_data=key) for key in button_keys if key in buttons_dict]
#    keyboard.add(*buttons)
#    return keyboard

@error_handler
def create_inline_keyboard(button_keys):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = []
    for key in button_keys:
        if key in buttons_dict:
            buttons.append(types.InlineKeyboardButton(text=buttons_dict[key], callback_data=key))
        else:
            if key.startswith('skip_question_'):
                buttons.append(types.InlineKeyboardButton(text='❌ Пропустить', callback_data=key))
            elif key.startswith('see_answer_'):
                buttons.append(types.InlineKeyboardButton(text='Узнать ответ 👀', callback_data=key))
            elif key.startswith('next_question_'):
                buttons.append(types.InlineKeyboardButton(text='❓ Следующий', callback_data=key))
            elif key.startswith('see_full_answer_'):
                buttons.append(types.InlineKeyboardButton(text='Объясни получше 💡', callback_data=key))
            elif key.startswith('again_wrong_and_skipped_'):
                buttons.append(types.InlineKeyboardButton(text='↺ Повторить', callback_data=key))
    keyboard.add(*buttons)
    return keyboard


def remove_timer_message(chat_id, message_id, index):
    time.sleep(timer_seconds)
    current_questions = read_current_questions(chat_id)
    stored_message_id = current_questions.get("timer_message_id")
    stored_state = current_questions.get("state")

    # Check if the message ID matches the stored timer message ID
    if message_id == stored_message_id:
        try:
            bot.delete_message(chat_id, message_id)
            current_questions["timer_message_id"] = None  # Update to None once deleted
            write_current_questions(chat_id, current_questions)
            bot.send_message(chat_id, "⏰ Время истекло. Помни, что тут ты тренируешься."
                                      " и в следующий раз у тебя получится!💪\n"
                                      "Ты можешь перейти к следующему вопросу "
                                      "или посмотреть ответ.",
                             reply_markup=create_inline_keyboard([f'next_question_{index}',f'see_answer_{index}','menu']))

        except Exception as e:
            print(f"Ошибка при удалении сообщения с таймером: {e}")





@error_handler
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    print(user_id)

     #если нет ссылки с параметром, а просто нажимаем /start
    try:# Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = "None"
        write_current_questions(user_id, current_questions)
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
    if tdb.has_user_answered(user_id):
        keyboard = create_inline_keyboard(['test_mode', 'statistics'])
    else:
        keyboard = create_inline_keyboard(['test_mode'])
    bot.send_message(message.chat.id, start_message, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'test_mode')
@error_handler
def handle_test_mode(call):
    user_id = call.from_user.id
    try:
        # Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = "None"
        write_current_questions(user_id, current_questions)
        #user_status = tdb.is_user_in_db(user_id)
        # проверяем, если пользователь неактивный (is_active = 0),
        # он имеет доступ к тренажеру только в разделе статистики
        # отказываем в доступе к Тестированию
        #if user_status == 0:
        #    keyboard = create_inline_keyboard(['menu'])
        #    bot.send_message(call.message.chat.id, 'У Вас нет доступа к Тестированию. Пожалуйста, обратитесь к куратору.', reply_markup=keyboard)
        #    return
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка при проверке пользователя: {e}")
        return

    keyboard = create_inline_keyboard(['all_questions', 'choose_topic', 'menu'])
    bot.send_message(call.message.chat.id, "Давайте начнём! Вы хотите отвечать на все вопросы из интервью или выбрать конкретную тему?", reply_markup=keyboard)
    # Здесь можно добавить логику для запуска тестирования

# Обработка кнопки "Статистика"

@bot.callback_query_handler(func=lambda call: call.data == 'menu')
@error_handler
def handle_menu(call):
    user_id = call.from_user.id
    user_status= tdb.is_user_in_db(user_id)

    current_questions = read_current_questions(user_id)

    if not current_questions.get("state").startswith("None_"):
        # Проверка и удаление сообщения с таймером, если нужно
        remove_timer_message_if_needed_for_call(call, user_id)

    current_questions = read_current_questions(user_id)
    current_questions["state"] = "None"
    write_current_questions(user_id, current_questions)


    # Создание клавиатуры и отправка сообщения
    #if user_status == 0:
    #    keyboard = create_inline_keyboard(['menu'])
    #    bot.send_message(call.message.chat.id, 'У Вас нет доступа к Тестированию. Пожалуйста, обратитесь к куратору.', reply_markup=keyboard)
    #    return
    if user_status == 0:
        keyboard = create_inline_keyboard(['test_mode', 'statistics', 'subscribe'])
        bot.send_message(call.message.chat.id, "Выберите раздел:", reply_markup=keyboard)
    else:
        keyboard = create_inline_keyboard(['test_mode', 'statistics'])
        bot.send_message(call.message.chat.id, "Выберите раздел:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == 'all_questions')
@error_handler
def handle_all_questions(call):
    filename = None
    user_id = call.from_user.id
    try:
        # Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = "all_questions"
        write_current_questions(user_id, current_questions)
        # Получаем количество правильно отвеченных вопросов и общее количество вопросов
        correct_answers_count, total_questions_count = tdb.get_correct_answers_count(user_id, "all")

        # Создаем прогресс-бар
        filename = draw_progress_bar(user_id, correct_answers_count, total_questions_count, 'all')
        bot.send_message(call.message.chat.id, f'Вы выбрали все вопросы.\n\nНапечатайте ответ '
                                               f'в поле ввода, или надиктуйте в микрофон.\n\nВаш ответ '
                                               f'мчит в ChatGPT 4о через сотни слоев и более'
                                               f' 10 миллиардов параметров. Пожалуйста, будьте '
                                               f'терпеливы, это может занять немного '
                                               f'времени.\n\nВаш прогресс:')
        time.sleep(2)

        with open(filename, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)


        # Добавляем задержку на 2 секунды
        #time.sleep(1)

        # Проверяем, ответил ли пользователь на все вопросы правильно
        if correct_answers_count == total_questions_count:
            # Отправка кастомного стикера по его идентификатору
            sticker_id = STICKER_HR  # Замените на настоящий идентификатор стикера
            bot.send_sticker(user_id, sticker_id)
            # Отправляем сообщение о завершении всех вопросов
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            repeat_button = types.InlineKeyboardButton(text='↺ Повторить', callback_data=f'repeat_all')
            choose_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
            keyboard.add(repeat_button, choose_button)
            bot.send_message(call.message.chat.id,
                             f'Поздравляем! Вы правильно ответили на все вопросы тренажера. Пора на интервью! Если хотите повторить вопросы, нажмите "Повторить".',
                             reply_markup=keyboard)
            return


        # Отправляем GIF таймера
        gif_path = 'GIF_timer/countdown.gif'
        with open(gif_path, 'rb') as gif:
            msg = bot.send_animation(call.message.chat.id, gif)

        # Сохраняем message_id сообщения с таймером и время его отправки
        current_questions = read_current_questions(user_id)
        current_questions["timer_message_id"] = msg.message_id
        current_questions["timer_start_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write_current_questions(user_id, current_questions)

        index='all'
        # Удаление таймера через 2 минуты
        threading.Thread(target=remove_timer_message, args=(call.message.chat.id, msg.message_id, index)).start()

        # Инициализация списка вопросов для пользователя из JSON файла
        current_questions = read_current_questions(user_id)



        key = f"all_{user_id}"
        if key not in current_questions["questions"] or not current_questions["questions"][key]:
            current_questions["questions"][key] = tdb.get_list_of_10_questions(user_id, "all")
            write_current_questions(user_id, current_questions)

        if not current_questions["questions"][key]:
            repeat_wrong_and_skipped_button = 'again_wrong_and_skipped_all'
            keyboard = create_inline_keyboard([repeat_wrong_and_skipped_button, 'menu'])
            bot.send_message(call.message.chat.id, "На сегодня для Вас больше нет"
                                                   " вопросов по этой теме."
                                                   " Вы можете повторить все пропущенные и "
                                                   "неправильно отвеченные вопросы, "
                                                   "или просто вернуться завтра!",
                                                    reply_markup=keyboard)
            return



        # Выбираем и отправляем случайный вопрос
        question_to_send = random.choice(current_questions["questions"][key])
        question_id, question_text = question_to_send
        keyboard = create_inline_keyboard(['skip_question_all', 'see_answer_all', 'menu'])
        bot.send_message(call.message.chat.id, f'Вопрос:\n\n❓{question_text}\n\n`', reply_markup=keyboard)

        # Сохраняем question_id последнего отправленного вопроса
        current_questions["last_question_id"] = question_id
        current_questions["last_question_text"] = question_text
        write_current_questions(user_id, current_questions)



        # Удаляем отправленный вопрос из всех списков
        remove_question_from_all_lists(user_id, question_id)



    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')

    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as remove_error:
                bot.send_message(call.message.chat.id, f'Не удалось удалить файл: {remove_error}')

@bot.callback_query_handler(func=lambda call: call.data.startswith('choose_topic'))
@error_handler
def choose_topic(call):
    global list_of_topics
    user_id = call.from_user.id
    # Установить состояние пользователя
    current_questions = read_current_questions(user_id)
    current_questions["state"] = "None"
    write_current_questions(user_id, current_questions)

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
@error_handler
def topic_selected(call):
    global list_of_topics
    filename = None
    user_id = call.from_user.id
    try:


        topic_index = int(call.data.split('_')[1])  # Извлекаем индекс выбранной темы
        topic_name = list_of_topics[topic_index]  # Получаем название темы по индексу

        # Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = f"topic_{topic_index}"

        write_current_questions(user_id, current_questions)

        # Получаем количество правильно отвеченных вопросов и общее количество вопросов по данной теме
        correct_answers_count, total_questions_count = tdb.get_correct_answers_count(user_id, topic_name)

        # Создаем прогресс-бар
        filename = draw_progress_bar(user_id, correct_answers_count, total_questions_count, topic_name)
        bot.send_message(call.message.chat.id, f'Вы выбрали тему: "{topic_name}".\n\nНапечатайте ответ '
                                               f'в поле ввода, или надиктуйте в микрофон.\n\nВаш ответ '
                                               f'мчит в ChatGPT 4о через сотни слоев и более'
                                               f' 10 миллиардов параметров. Пожалуйста, будьте '
                                               f'терпеливы, это может занять немного '
                                               f'времени.\n\n Ваш прогресс:')
        time.sleep(2)

        with open(filename, 'rb') as photo:
            bot.send_photo(call.message.chat.id, photo)
        # Добавляем задержку на 2 секунды
        #time.sleep(1)
        # Проверяем, ответил ли пользователь на все вопросы правильно
        if correct_answers_count == total_questions_count:
            # Отправка кастомного стикера по его идентификатору
            sticker_id = STICKER_SUCCESS  # Замените на настоящий идентификатор стикера
            bot.send_sticker(user_id, sticker_id)
            # Отправляем сообщение о завершении всех вопросов
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            repeat_button = types.InlineKeyboardButton(text='↺ Повторить', callback_data=f'repeat_{topic_index}')
            choose_button = types.InlineKeyboardButton(text='Выбрать тему', callback_data='choose_topic')
            keyboard.add(repeat_button, choose_button)
            bot.send_message(call.message.chat.id,
                             f'🚀 Вы - пример движения к цели! Вы правильно ответили на все вопросы из темы "{topic_name}". Если хотите повторить тему снова, нажмите "Повторить".',
                             reply_markup=keyboard)
            return

        # Отправляем GIF таймера
        gif_path = 'GIF_timer/countdown.gif'
        with open(gif_path, 'rb') as gif:
            msg = bot.send_animation(call.message.chat.id, gif)

        # Сохраняем message_id сообщения с таймером и время его отправки
        current_questions = read_current_questions(user_id)
        current_questions["timer_message_id"] = msg.message_id
        current_questions["timer_start_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write_current_questions(user_id, current_questions)


        # Удаление таймера через 2 минуты
        threading.Thread(target=remove_timer_message, args=(call.message.chat.id, msg.message_id, topic_index)).start()

        # Инициализация списка вопросов для пользователя из JSON файла
        current_questions = read_current_questions(user_id)



        # Заполнение списка вопросов для пользователя по выбранной теме

        key = f"{topic_name}_{user_id}"
        if key not in current_questions["questions"] or not current_questions["questions"][key]:
            current_questions["questions"][key] = tdb.get_list_of_10_questions(user_id, topic_name)
            write_current_questions(user_id, current_questions)

        if not current_questions["questions"][key]:
            try:
                timer_message_id = current_questions.get("timer_message_id")
                if timer_message_id:
                    bot.delete_message(call.message.chat.id, timer_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения с таймером: {e}")

            # Выводим данные из callback-запроса для отладки



            keyboard = types.InlineKeyboardMarkup(row_width=2)
            repeat_button = types.InlineKeyboardButton(text='↺ Повторить', callback_data=f'again_wrong_and_skipped_{topic_index}')
            choose_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
            keyboard.add(repeat_button, choose_button)

            bot.send_message(call.message.chat.id,
                             "На сегодня для Вас больше нет"
                                                   " вопросов по этой теме."
                                                   " Вы можете повторить все пропущенные и "
                                                   "неправильно отвеченные вопросы, "
                                                   "или просто вернуться завтра!",
                                                    reply_markup=keyboard)
            return





        # Выбираем и отправляем случайный вопрос
        question_to_send = random.choice(current_questions["questions"][key])
        question_id, question_text = question_to_send
        # Генерация ключа и текста для кнопки "Пропустить"
        skip_button_key, skip_button_text = create_skip_question_button(topic_index)

        # Проверка создания клавиатуры с кнопками

        see_answer_key, see_answer_text = create_see_answer_button(topic_index)

        keyboard = create_inline_keyboard([skip_button_key, see_answer_key, 'menu'])



        bot.send_message(call.message.chat.id, f'Вопрос по теме "{topic_name}":\n\n❓{question_text}\n\n `',
                         reply_markup=keyboard)


        # Сохраняем question_id последнего отправленного вопроса
        current_questions["last_question_id"] = question_id
        current_questions["last_question_text"] = question_text
        write_current_questions(user_id, current_questions)

        # Удаляем отправленный вопрос из всех списков
        remove_question_from_all_lists(user_id, question_id)

    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')

    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as remove_error:
                bot.send_message(call.message.chat.id, f'Не удалось удалить файл: {remove_error}')




def remove_timer_message_if_needed_for_call(call, user_id):
    current_questions = read_current_questions(user_id)
    timer_message_id = current_questions.get("timer_message_id")
    timer_start_time = current_questions.get("timer_start_time")

    if timer_message_id and timer_start_time:
        timer_start_time = datetime.strptime(timer_start_time, '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - timer_start_time).total_seconds() < timer_seconds:
            try:
                chat_id = call.message.chat.id
                bot.delete_message(chat_id, timer_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения с таймером: {e}")


def remove_timer_message_if_needed_for_message(message, user_id):
    current_questions = read_current_questions(user_id)
    timer_message_id = current_questions.get("timer_message_id")
    timer_start_time = current_questions.get("timer_start_time")

    if timer_message_id and timer_start_time:
        timer_start_time = datetime.strptime(timer_start_time, '%Y-%m-%d %H:%M:%S')
        if (datetime.now() - timer_start_time).total_seconds() < timer_seconds:
            try:
                chat_id = message.chat.id
                bot.delete_message(chat_id, timer_message_id)
            except Exception as e:
                print(f"Ошибка при удалении сообщения с таймером: {e}")





@bot.callback_query_handler(func=lambda call: call.data.startswith('skip_question'))
@error_handler
def handle_skip_question(call):

    user_id = call.from_user.id
    today_date = datetime.now().strftime('%Y-%m-%d')

    try:


        topic_index = int(call.data.split('_')[2]) if call.data != 'skip_question_all' else 'all'

        # Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = f"skip_question_{topic_index}"
        write_current_questions(user_id, current_questions)

        topic_name = list_of_topics[topic_index] if topic_index != 'all' else 'all'
        current_questions = read_current_questions(user_id)
        question_id = current_questions.get("last_question_id")


        if question_id is None:
            bot.send_message(call.message.chat.id, "Не удалось найти идентификатор последнего вопроса.")
            return

        # Добавляем запись в таблицу Answers
        tdb.add_skipped_question(user_id, question_id, today_date)

        bot.send_message(call.message.chat.id, "Вопрос был пропущен.")

        # Проверка и удаление сообщения с таймером, если нужно
        remove_timer_message_if_needed_for_call(call, user_id)

        # Определяем, является ли пропуск для всех вопросов или для конкретной темы
        key = f"all_{user_id}" if topic_index == 'all' else f"{topic_name}_{user_id}"

        # Проверяем, есть ли еще вопросы в текущем списке
        if not current_questions["questions"][key]:
            current_questions["questions"][key] = tdb.get_list_of_10_questions(user_id, topic_name)
            write_current_questions(user_id, current_questions)

        # Отправляем GIF таймера
        gif_path = 'GIF_timer/countdown.gif'
        with open(gif_path, 'rb') as gif:
            msg = bot.send_animation(call.message.chat.id, gif)

        # Сохраняем message_id сообщения с таймером и время его отправки
        current_questions = read_current_questions(user_id)
        current_questions["timer_message_id"] = msg.message_id
        current_questions["timer_start_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write_current_questions(user_id, current_questions)


        # Удаление таймера через 2 минуты
        threading.Thread(target=remove_timer_message, args=(call.message.chat.id, msg.message_id, topic_index)).start()

        # Отправляем следующий вопрос
        if current_questions["questions"][key]:
            question_to_send = random.choice(current_questions["questions"][key])
            question_id, question_text = question_to_send
            # Генерация ключа и текста для кнопки "Пропустить"
            skip_button_key = f'skip_question_{topic_index}' if topic_index != "all" else 'skip_question_all'
            see_answer_key = f'see_answer_{topic_index}' if topic_index != "all" else 'see_answer_all'

            keyboard = create_inline_keyboard([skip_button_key, see_answer_key, 'menu'])
            bot.send_message(call.message.chat.id, f'Вопрос:\n\n❓{question_text}\n\n`', reply_markup=keyboard)

            # Сохраняем question_id последнего отправленного вопроса
            current_questions["last_question_id"] = question_id
            current_questions["last_question_text"] = question_text
            write_current_questions(user_id, current_questions)

            # Удаляем отправленный вопрос из всех списков
            remove_question_from_all_lists(user_id, question_id)
        else:
            repeat_wrong_and_skipped_button = f'again_wrong_and_skipped_{topic_index}' if topic_index != "all" else 'again_wrong_and_skipped_all'
            print(repeat_wrong_and_skipped_button)
            keyboard = create_inline_keyboard([repeat_wrong_and_skipped_button,'menu'])
            bot.send_message(call.message.chat.id, "На сегодня для Вас больше нет"
                                                   " вопросов по этой теме."
                                                   " Вы можете повторить все пропущенные и "
                                                   "неправильно отвеченные вопросы, "
                                                   "или просто вернуться завтра!", reply_markup=keyboard)


    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('see_answer'))
@error_handler
def handle_see_answer(call):
    user_id = call.from_user.id
    today_date = datetime.now().strftime('%Y-%m-%d')
    bot.send_message(call.message.chat.id, 'Формируем идеальный ответ. Подождите, пожалуйста.🧘')

    try:



        topic_index = int(call.data.split('_')[2]) if call.data != 'see_answer_all' else 'all'

        # Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = "None"
        write_current_questions(user_id, current_questions)

        topic_name = list_of_topics[topic_index] if topic_index != 'all' else 'all'

        current_questions = read_current_questions(user_id)
        question_id = current_questions.get("last_question_id")


        if question_id is None:
            bot.send_message(call.message.chat.id, "Не удалось найти идентификатор последнего вопроса.")
            return

        # Добавляем запись в таблицу Answers
        tdb.add_skipped_question(user_id, question_id, today_date)

        # Проверка и удаление сообщения с таймером, если нужно
        remove_timer_message_if_needed_for_call(call, user_id)

        # Определяем, является ли запрос ответа для всех вопросов или для конкретной темы
        if call.data == 'see_answer_all':
            key = f"all_{user_id}"
            question_topic = "all"
        else:
            topic_id = int(call.data.split('_')[-1])
            question_topic = list_of_topics[topic_id]
            key = f"{question_topic}_{user_id}"

        #Запрашиваем ответ у ЧатаГПТ без консультации с БД
        question_text = current_questions["last_question_text"]

        correct_answer = question_answer_from_ChatGPT(question_text)


        ## Проверяем наличие правильного ответа в базе данных
        #correct_answer = tdb.get_correct_answer(question_id)
        #if correct_answer is None:
        #    # Если правильного ответа нет, запрашиваем его с помощью GPT-3
        #    question_text = current_questions["last_question_text"]
        #    correct_answer = question_answer_from_ChatGPT(question_text)




        # Разбиваем ответ на части и отправляем
        max_length = 4096
        for i in range(0, len(correct_answer), max_length):
            bot.send_message(call.message.chat.id, correct_answer[i:i+max_length])

        next_question_key, next_question_text = create_next_question_button(topic_index)
        see_full_answer_key, see_full_answer_text = create_see_full_answer_button(topic_index)



        # Добавляем кнопки "Следующий вопрос" и "Главное меню"
        see_full_answer_button = see_full_answer_key if question_topic != "all" else 'see_full_answer_all'
        next_question_button = next_question_key if question_topic != "all" else 'next_question_all'
        keyboard = create_inline_keyboard([next_question_button, 'menu', see_full_answer_button])
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)

    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('see_full_answer'))
@error_handler
def handle_see_full_answer(call):
    user_id = call.from_user.id
    today_date = datetime.now().strftime('%Y-%m-%d')
    bot.send_message(call.message.chat.id, 'Сейчас я объясню в подробностях.🔍 Подождите, пожалуйста.')

    try:



        topic_index = int(call.data.split('_')[3]) if call.data != 'see_full_answer_all' else 'all'

        # Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = "None"
        write_current_questions(user_id, current_questions)

        topic_name = list_of_topics[topic_index] if topic_index != 'all' else 'all'

        current_questions = read_current_questions(user_id)
        question_id = current_questions.get("last_question_id")


        if question_id is None:
            bot.send_message(call.message.chat.id, "Не удалось найти идентификатор последнего вопроса.")
            return



        # Определяем, является ли запрос ответа для всех вопросов или для конкретной темы
        if call.data == 'see_full_answer_all':
            key = f"all_{user_id}"
            question_topic = "all"
        else:
            topic_id = int(call.data.split('_')[-1])
            question_topic = list_of_topics[topic_id]
            key = f"{question_topic}_{user_id}"

        #Запрашиваем ответ у ЧатаГПТ без консультации с БД
        question_text = current_questions["last_question_text"]

        detailed_answer = question_detailed_answer_from_ChatGPT(question_text)


        ## Проверяем наличие правильного ответа в базе данных
        #correct_answer = tdb.get_correct_answer(question_id)
        #if correct_answer is None:
        #    # Если правильного ответа нет, запрашиваем его с помощью GPT-3
        #    question_text = current_questions["last_question_text"]
        #    correct_answer = question_answer_from_ChatGPT(question_text)




        # Разбиваем ответ на части и отправляем
        max_length = 4096
        for i in range(0, len(detailed_answer), max_length):
            bot.send_message(call.message.chat.id, detailed_answer[i:i+max_length])

        next_question_key, next_question_text = create_next_question_button(topic_index)



        # Добавляем кнопки "Следующий вопрос" и "Главное меню"
        next_question_button = next_question_key if question_topic != "all" else 'next_question_all'
        keyboard = create_inline_keyboard([next_question_button, 'menu'])
        bot.send_message(call.message.chat.id, "Выберите действие:", reply_markup=keyboard)

    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')

@bot.callback_query_handler(func=lambda call: call.data.startswith('next_question'))
@error_handler
def handle_next_question(call):
    user_id = call.from_user.id
    filename = None
    try:

        # Определяем, является ли запрос для всех вопросов или для конкретной темы
        if call.data == 'next_question_all':
            key = f"all_{user_id}"
            topic_name = "all"
            topic_index = "all"
            state = "next_question_all"
        else:
            topic_index = int(call.data.split('_')[-1])
            topic_name = list_of_topics[topic_index]
            key = f"{topic_name}_{user_id}"
            state = f"next_question_{topic_index}"

        # Установить состояние пользователя
        current_questions = read_current_questions(user_id)
        current_questions["state"] = state
        write_current_questions(user_id, current_questions)




        # Инициализация списка вопросов для пользователя из JSON файла
        current_questions = read_current_questions(user_id)

        if not current_questions["questions"].get(key):
            current_questions["questions"][key] = tdb.get_list_of_10_questions(user_id, topic_name)
            write_current_questions(user_id, current_questions)

        if not current_questions["questions"][key]:
            repeat_wrong_and_skipped_button = f'again_wrong_and_skipped_{topic_index}' if topic_index != "all" else 'again_wrong_and_skipped_all'
            keyboard = create_inline_keyboard([repeat_wrong_and_skipped_button, 'menu'])
            bot.send_message(call.message.chat.id, "На сегодня для Вас больше нет"
                                                   " вопросов по этой теме."
                                                   " Вы можете повторить все пропущенные и "
                                                   "неправильно отвеченные вопросы, "
                                                   "или просто вернуться завтра!", reply_markup=keyboard)
            return

        # Отправляем GIF таймера

        gif_path = 'GIF_timer/countdown.gif'
        with open(gif_path, 'rb') as gif:
            msg = bot.send_animation(call.message.chat.id, gif)

        # Сохраняем message_id сообщения с таймером и время его отправки
        current_questions = read_current_questions(user_id)
        current_questions["timer_message_id"] = msg.message_id
        current_questions["timer_start_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write_current_questions(user_id, current_questions)


        # Удаление таймера через 2 минуты
        threading.Thread(target=remove_timer_message, args=(call.message.chat.id, msg.message_id, topic_index)).start()

        # Выбираем и отправляем случайный вопрос
        question_to_send = random.choice(current_questions["questions"][key])
        question_id, question_text = question_to_send
        if topic_name == "all":
            keyboard = create_inline_keyboard(['skip_question_all', 'see_answer_all', 'menu'])
        else:
            skip_button_key, skip_button_text = create_skip_question_button(topic_index)

            see_answer_key, see_answer_text = create_see_answer_button(topic_index)

            keyboard = create_inline_keyboard([skip_button_key, see_answer_key, 'menu'])

        bot.send_message(call.message.chat.id, f'Вопрос по теме "{topic_name}":\n\n❓{question_text}\n\n`', reply_markup=keyboard)

        # Сохраняем question_id последнего отправленного вопроса
        current_questions["last_question_id"] = question_id
        current_questions["last_question_text"] = question_text
        write_current_questions(user_id, current_questions)

        # Удаляем отправленный вопрос из всех списков
        remove_question_from_all_lists(user_id, question_id)

    except Exception as e:
        bot.send_message(call.message.chat.id, f'Произошла ошибка: {e}')

    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception as remove_error:
                bot.send_message(call.message.chat.id, f'Не удалось удалить файл: {remove_error}')


@bot.callback_query_handler(func=lambda call: call.data.startswith('repeat'))
@error_handler
def handle_repeat(call):
    user_id = call.from_user.id

    # Установить состояние пользователя
    current_questions = read_current_questions(user_id)
    current_questions["state"] = "None"
    write_current_questions(user_id, current_questions)

    data = call.data.split('_')
    if len(data) == 2 and data[1] == 'all':
        # Повтор всех вопросов
        tdb.reset_answers_for_user(user_id)

        # Предлагаем пользователю начать тестирование или выбрать тему
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        test_button = types.InlineKeyboardButton(text='Все вопросы', callback_data='all_questions')
        choose_button = types.InlineKeyboardButton(text='Выбрать тему', callback_data='choose_topic')
        menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
        keyboard.add(choose_button, test_button, menu_button)
        bot.send_message(call.message.chat.id, 'Все вопросы были сброшены. Вы можете начать заново.', reply_markup=keyboard)
    elif len(data) == 2:
        # Повтор вопросов по конкретной теме
        topic_index = int(data[1])
        topic_name = list_of_topics[topic_index]
        tdb.reset_answers_for_user(user_id, topic_name)
        # Предлагаем пользователю начать тестирование или выбрать тему
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        test_button = types.InlineKeyboardButton(text='Все вопросы', callback_data='all_questions')
        choose_button = types.InlineKeyboardButton(text='Выбрать тему', callback_data='choose_topic')
        menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
        keyboard.add(choose_button, test_button,  menu_button)
        bot.send_message(call.message.chat.id, f'Все вопросы по теме "{topic_name}" были сброшены. Вы можете начать заново.', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('again_wrong_and_skipped'))
@error_handler
def handle_repeat_wrong_and_skipped(call):
    # Выводим данные из callback-запроса для отладки

    user_id = call.from_user.id


    # Установить состояние пользователя
    current_questions = read_current_questions(user_id)
    current_questions["state"] = "None"
    write_current_questions(user_id, current_questions)


    data = call.data.split('_')



    if len(data) == 5 and data[4] == 'all':
        # Повтор всех вопросов

        tdb.repeat_wrong_and_skipped_questions(user_id)

        # Предлагаем пользователю начать тестирование или выбрать тему
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        test_button = types.InlineKeyboardButton(text='Все вопросы', callback_data='all_questions')
        choose_button = types.InlineKeyboardButton(text='Выбрать тему', callback_data='choose_topic')
        menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
        keyboard.add(choose_button, test_button, menu_button)
        bot.send_message(call.message.chat.id,
                         'Все неверные и пропущенные вопросы были сброшены. Вы можете начать заново.',
                         reply_markup=keyboard)
    elif len(data) == 5:
        # Повтор вопросов по конкретной теме
        topic_index = int(data[4])
        topic_name = list_of_topics[topic_index]
        tdb.repeat_wrong_and_skipped_questions(user_id, topic_name)
        # Предлагаем пользователю начать тестирование или выбрать тему
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        test_button = types.InlineKeyboardButton(text='Все вопросы', callback_data='all_questions')
        choose_button = types.InlineKeyboardButton(text='Выбрать тему', callback_data='choose_topic')
        menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
        keyboard.add(choose_button, test_button, menu_button)
        bot.send_message(call.message.chat.id,
                         f'Все неверные и пропущенные вопросы по теме "{topic_name}" были сброшены. Вы можете начать заново.',
                         reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data == 'cancel_reminder')
@error_handler
def handle_cancel_reminder(call):
    user_id = call.from_user.id

    # Деактивировать пользователя
    tdb.deactivate_user(user_id)

    # Создание клавиатуры с кнопками
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    subscribe_button = types.InlineKeyboardButton(text='Включить напоминания 🔔', callback_data='subscribe')
    menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
    keyboard.add(subscribe_button, menu_button)

    # Отправка сообщения с кнопками
    bot.send_message(call.message.chat.id, 'Ты отписался от напоминаний, и я буду скучать\\! 🐾😿\n'
                                            'А пока я пошел выбирать себе элитный корм,'
                                            'который подобает есть коту успешного программиста\\.\nНажми '
                                           '"Включить напоминания" и я помогу тебе не '
                                           'забыть про ~корм~🥣 Питонячие вопросы\\!',
                                            parse_mode='MarkdownV2',
                                            reply_markup=keyboard)





@bot.callback_query_handler(func=lambda call: call.data == 'subscribe')
@error_handler
def handle_subscribe(call):
    user_id = call.from_user.id

    # Активировать пользователя
    tdb.activate_user(user_id)

    # Создание клавиатуры с кнопками
    keyboard = create_inline_keyboard(['menu'])
    # Отправка кастомного стикера (котика) по его идентификатору
    sticker_id = STICKER_CAT  # Замените на настоящий идентификатор стикера
    bot.send_sticker(user_id, sticker_id)
    # Отправка сообщения с кнопками
    bot.send_message(call.message.chat.id, 'Ура! Ты подписался на напоминания и мы снова вместе! 🐾😺 '
                                       'Я помогу тебе не забыть про мечту стать успешным программистом.'
                                       ' Вдвоём к успеху! 🚀', reply_markup=keyboard)
#STATISTICS



def get_progress(user_id, list_of_topics):
    statistics = {}

    # Статистика по темам
    topic_stats = {
        'Тема': [],
        'Верно': [],
        'Всего': []
    }

    for topic in list_of_topics:
        correct_answers_count, total_questions_count = tdb.get_correct_answers_count(user_id, topic)
        statistics[topic] = (correct_answers_count, total_questions_count)
        topic_stats['Тема'].append(topic)
        topic_stats['Верно'].append(correct_answers_count)
        topic_stats['Всего'].append(total_questions_count)

    # Получение общей статистики по всем темам
    correct_answers_count_all, total_questions_count_all = tdb.get_correct_answers_count(user_id, "all")
    statistics["all"] = (correct_answers_count_all, total_questions_count_all)

    # Добавление строки "Все темы" в начало
    topic_stats['Тема'].insert(0, 'Все темы')
    topic_stats['Верно'].insert(0, correct_answers_count_all)
    topic_stats['Всего'].insert(0, total_questions_count_all)

    topics_df = pd.DataFrame(topic_stats)
    return topics_df

def create_progress_image(df):
    # Настройка размеров колонок и высоты строки заголовка
    tema_width = 0.7  # Ширина столбца "Тема"
    correctly_width = 0.25  # Ширина столбца "Верно"
    total_width = 0.25  # Ширина столбца "Всего"
    header_height = 0.08  # Высота строки заголовка в процентах от общей высоты

    fig, ax = plt.subplots(figsize=(8, len(df) * 0.5 + 1))
    fig.patch.set_facecolor('#6C3483')  # Установка черного фона для всей фигуры
    ax.axis('tight')
    ax.axis('off')

    # Создание таблицы
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')

    # Установка размеров шрифта и высоты строк
    table.auto_set_font_size(False)
    table.set_fontsize(14)


    # Раскраска строк таблицы
    colors = ['#6C3483', '#d0f0c0', '#D3D3D3']  # Цвета строк: черный, фиолетовый, зеленый #ABEBC6
    text_colors = ['#FFFFFF', '#000000', '#000000']  # Цвета текста: белый, белый, черный

    for key, cell in table.get_celld().items():
        if key[0] == 0:  # заголовок
            cell.set_fontsize(20)
            cell.set_height(header_height)
            cell.set_text_props(weight='bold')  # Сделать заголовки жирными
            cell.set_facecolor(colors[0])
            cell.set_text_props(color=text_colors[0])

        elif key[0] == 1:  # строка "Все темы"
            cell.set_facecolor(colors[1])
            cell.set_text_props(color=text_colors[1])
            cell.set_fontsize(20)
            cell.set_height(0.045)
        else:  # остальные строки
            cell.set_facecolor(colors[2])
            cell.set_text_props(color=text_colors[2])
            cell.set_fontsize(20)
            cell.set_height(0.045)

        if key[1] == 0:  # Первый столбец "Тема"
            cell.set_width(tema_width)
        elif key[1] == 1:  # Второй столбец "Верно"
            cell.set_width(correctly_width)
        elif key[1] == 2:  # Третий столбец "Всего"
            cell.set_width(total_width)

    # Установка равных отступов слева и справа
    fig.tight_layout(pad=1.0)

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img = Image.open(buf)
    return img

# Обработчик для статистики

# Обработчик для статистики
# Обработчик для статистики
@bot.callback_query_handler(func=lambda call: call.data == 'statistics')
@error_handler
def handle_statistics(call):
    user_id = call.from_user.id
    global list_of_topics
    topics_df = get_progress(user_id, list_of_topics)

    # Установить состояние пользователя
    current_questions = read_current_questions(user_id)
    current_questions["state"] = "None"
    write_current_questions(user_id, current_questions)

    # Создание изображения с таблицей
    img = create_progress_image(topics_df)

    # Отправка изображения
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    bot.send_photo(call.message.chat.id, buf, caption="Ваш общий прогресс")

    keyboard = create_inline_keyboard(['detailed_statistics', 'menu'])
    bot.send_message(call.message.chat.id, "Для более детальной информации выберите 'Подробный отчет'", reply_markup=keyboard)


#STATISTICS TEXT
# Функция для создания текстового отчета
# Функция для создания текстового отчета
def get_text_progress_report(user_id, list_of_topics):
    report_lines = []

    # Получаем статистику по всем темам
    topics_df = get_progress(user_id, list_of_topics)

    for index, row in topics_df.iterrows():
        topic = row['Тема']
        correct = row['Верно']
        total = row['Всего']

        avg_attempts = tdb.get_average_attempts(user_id, topic if topic != 'Все темы' else None)
        last_answer_date = tdb.get_last_answer_date(user_id, topic if topic != 'Все темы' else None)

        correct_week = tdb.get_correct_answers_count_period(user_id, topic if topic != 'Все темы' else None, days=7)
        correct_month = tdb.get_correct_answers_count_period(user_id, topic if topic != 'Все темы' else None, days=30)
        total_attempts_week, total_attempts_month = tdb.get_total_attempts(user_id,
                                                                           topic if topic != 'Все темы' else None)
        incorrect_count_week = tdb.get_incorrect_answers_count_period(user_id, topic if topic != 'Все темы' else None, days=7)
        incorrect_count_month = tdb.get_incorrect_answers_count_period(user_id, topic if topic != 'Все темы' else None, days=30)
        skipped_count_week = tdb.get_skipped_answers_count_period(user_id, topic if topic != 'Все темы' else None, days=7)
        skipped_count_month = tdb.get_skipped_answers_count_period(user_id, topic if topic != 'Все темы' else None, days=30)


        # Функция для выбора правильного падежа слова "раз"
        def get_raz_word(count):
            if count % 10 == 1 and count % 100 != 11:
                return "раз"
            elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
                return "раза"
            else:
                return "раз"
        # Добавляем пунктирную линию
        report_lines.append('-' * 32)
        report_lines.append(topic)
        report_lines.append('-' * 32)
        report_lines.append(f"Правильно за неделю / месяц:  {correct_week} / {correct_month}.")

        report_lines.append(f"Правильно за все время:  {correct}")
        report_lines.append(f"Неправильно за неделю / месяц: {incorrect_count_week} / {incorrect_count_month}.")

        report_lines.append(f"Пропущенные вопросы за неделю / месяц: {skipped_count_week} / {skipped_count_month}.")

        report_lines.append(f"Всего вопросов по теме:  {total}")
        report_lines.append(f"Вы правильно отвечаете на вопрос в среднем с {avg_attempts} попытки.")
        report_lines.append(f"Последний раз Вы отвечали на вопрос этого раздела {last_answer_date}.")


    return report_lines


# Функция для отправки сообщений
def send_report_messages(bot, chat_id, report_lines):
    message = ""
    for line in report_lines:
        if len(message) + len(line) > 4000:
            bot.send_message(chat_id, message)
            message = ""
        message += line + "\n"
    if message:
        bot.send_message(chat_id, message)

# Обработчик для отчетов
@bot.callback_query_handler(func=lambda call: call.data == 'detailed_statistics')
def handle_text_report(call):
    user_id = call.from_user.id

    # Установить состояние пользователя
    current_questions = read_current_questions(user_id)
    current_questions["state"] = "None"
    write_current_questions(user_id, current_questions)

    list_of_topics = tdb.get_all_topics()
    report_lines = get_text_progress_report(user_id, list_of_topics)
    keyboard = create_inline_keyboard(['menu'])
    send_report_messages(bot, call.message.chat.id, report_lines)
    bot.send_message(call.message.chat.id, "Продолжайте в том же духе!",
                     reply_markup=keyboard)

#REMINDER

# Функция для отправки напоминаний пользователям
def send_reminders():

    inactive_users = tdb.get_inactive_users()

    for user_id, last_answer_date in inactive_users:
        days = days_since_last_answer(last_answer_date)
        day_word = get_day_word(days)
        # Отправка кастомного стикера по его идентификатору
        sticker_id = STICKER_CAT  # Замените на настоящий идентификатор стикера
        bot.send_sticker(user_id, sticker_id)

        reminder_text = f"❗❗Прошло уже {days} {day_word}, как ты не идешь в направлении мечты. Погладь меня и пойдем тренироваться?"

        keyboard = types.InlineKeyboardMarkup(row_width=2)
        test_button = types.InlineKeyboardButton(text='❓ Тестирование', callback_data='test_mode')
        menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
        cancel_button = types.InlineKeyboardButton(text='Отключить напоминания 🔕', callback_data='cancel_reminder')
        keyboard.add(test_button, menu_button, cancel_button)

        bot.send_message(user_id, reminder_text, reply_markup=keyboard)




# Функция для запуска расписания
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Настройка расписания
schedule.every().day.at("02:01").do(send_reminders)


#VOICE


# Ваш API ключ для OpenAI
#OPENAI_API_KEY = WHISPER_API
# OpenAI API key
client = OpenAI(api_key=UNIVERSITY_OPEN_API,
                base_url="https://api.proxyapi.ru/openai/v1")
#client = OpenAI(api_key=OPENAI_API_KEY)

# Укажите полный путь к ffmpeg.exe

FFMPEG_PATH = LINUX_FFMPEG_PATH
# Создание папки для аудиофайлов
audio_folder = os.path.join(os.path.dirname(__file__), "user_voice_messages")
os.makedirs(audio_folder, exist_ok=True)

#если линукс, то
@error_handler
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    user_id = message.from_user.id
    mp3_file_path = None
    ogg_file_path = None

    try:
        current_questions = read_current_questions(user_id)
        # Получаем текст последнего вопроса
        last_question_text = current_questions.get("last_question_text")
        last_question_id = current_questions.get("last_question_id")
        state = current_questions.get("state")


        if not current_questions.get("state").startswith("None"):  # Проверка состояния пользователя
            # Скачиваем голосовое сообщение
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем голосовое сообщение во временный файл
            ogg_file_path = os.path.join(audio_folder, f"voice_message_{user_id}.ogg")
            mp3_file_path = os.path.join(audio_folder, f"voice_message_{user_id}.mp3")

            with open(ogg_file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Преобразуем формат файла из ogg в mp3
            subprocess.run([FFMPEG_PATH, "-i", ogg_file_path, mp3_file_path], stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           text=True, timeout=30)

            question_topic = tdb.get_question_topic(last_question_id)
            topic_index = 'all'

            if question_topic in list_of_topics:
                topic_index = list_of_topics.index(question_topic)

            # Создание словаря с этими переменными в строку
            whisper_prompt = {
                0: prompt_0, 1: prompt_1, 2: prompt_2, 3: prompt_3, 4: prompt_4, 5: prompt_5, 6: prompt_6,
                7: prompt_7, 8: prompt_8, 9: prompt_9, 10: prompt_10, 11: prompt_11, 12: prompt_12,
                13: prompt_13, 14: prompt_14, 15: prompt_15, 16: prompt_16, 17: prompt_17, 18: prompt_18,
                19: prompt_19, 20: prompt_20, 21: prompt_21, 22: prompt_22, "all": prompt_all
            }




            # Динамически получаем нужный промпт
            TOPIC_PROMPT = whisper_prompt.get(topic_index, whisper_prompt["all"])

            # Открываем mp3 файл для транскрипции
            with open(mp3_file_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    prompt = TOPIC_PROMPT

                )

        # Отправляем транскрибированный текст пользователю
            bot.reply_to(message, transcription.text)

            # Проверка и удаление сообщения с таймером, если нужно
            remove_timer_message_if_needed_for_message(message, user_id)

            # Получаем обратную связь на ответ пользователя


            feedback = get_feedback(last_question_text, transcription.text)
            bot.send_message(message.chat.id, feedback)

            # Обновляем запись в таблице Answers
            question_id = current_questions.get("last_question_id")
            success=tdb.update_answer_record(user_id, question_id, feedback)
            if success == 1:
                sticker_id = STICKER_THUMBS_UP_CAT  # Замените на настоящий идентификатор стикера
                bot.send_sticker(user_id, sticker_id)

            # Добавляем кнопки "Следующий вопрос" в зависимости от состояния
            if state == 'all_questions':
                next_question_button = 'next_question_all'
            elif state.startswith('topic_'):
                topic_index = state.split('_')[1]
                next_question_button = f'next_question_{topic_index}'
            elif state.startswith('skip_question_'):
                topic_index = state.split('_')[2] if state != 'skip_question_all' else 'all'
                next_question_button = f'next_question_{topic_index}' if topic_index != 'all' else 'next_question_all'
            elif state.startswith('next_question_'):
                topic_index = state.split('_')[2] if state != 'next_question_all' else 'all'
                next_question_button = f'next_question_{topic_index}' if topic_index != 'all' else 'next_question_all'
            else:
                next_question_button = 'menu'  # на случай, если состояние не соответствует ожидаемым

            keyboard = create_inline_keyboard([next_question_button, 'menu'])
            bot.send_message(message.chat.id, "Продолжим вопросы?", reply_markup=keyboard)


        else:
            keyboard = create_inline_keyboard(['menu'])
            bot.reply_to(message, "Вы можете печатать или записывать голосовые сообщения только после вопроса.", reply_markup=keyboard)

    except Exception as e:
        # Обработка любых ошибок
        bot.reply_to(message, "Ошибка транскрибации. Попробуйте записать сообщение снова либо введите текст.")
        print(f"Произошла ошибка: {e}")

    finally:
        # Удаляем временные файлы, если они были созданы
        if ogg_file_path and os.path.exists(ogg_file_path):
            os.remove(ogg_file_path)
        if mp3_file_path and os.path.exists(mp3_file_path):
            os.remove(mp3_file_path)

@error_handler
@bot.message_handler(content_types=['text'])
def handle_text(message):
    user_id = message.from_user.id

    try:
        current_questions = read_current_questions(user_id)
        last_question_text = current_questions.get("last_question_text")
        state = current_questions.get("state")

        if not current_questions.get("state").startswith("None"):
            user_response = message.text
            # Проверка и удаление сообщения с таймером, если нужно
            remove_timer_message_if_needed_for_message(message, user_id)

            feedback = get_feedback(last_question_text, user_response)
            bot.send_message(message.chat.id, feedback)

            # Обновляем запись в таблице Answers
            question_id = current_questions.get("last_question_id")
            success=tdb.update_answer_record(user_id, question_id, feedback)
            if success == 1:
                sticker_id = STICKER_THUMBS_UP_CAT  # Замените на настоящий идентификатор стикера
                bot.send_sticker(user_id, sticker_id)

            # Добавляем кнопки "Следующий вопрос" в зависимости от состояния
            if state == 'all_questions':
                next_question_button = 'next_question_all'
            elif state.startswith('topic_'):
                topic_index = state.split('_')[1]
                next_question_button = f'next_question_{topic_index}'
            elif state.startswith('skip_question_'):
                topic_index = state.split('_')[2] if state != 'skip_question_all' else 'all'
                next_question_button = f'next_question_{topic_index}' if topic_index != 'all' else 'next_question_all'
            elif state.startswith('next_question_'):
                topic_index = state.split('_')[2] if state != 'next_question_all' else 'all'
                next_question_button = f'next_question_{topic_index}' if topic_index != 'all' else 'next_question_all'
            else:
                next_question_button = 'menu' # на случай, если состояние не соответствует ожидаемым

            keyboard = create_inline_keyboard([next_question_button, 'menu'])
            bot.send_message(message.chat.id, "Продолжим вопросы?", reply_markup=keyboard)
        else:
            keyboard = create_inline_keyboard(['menu'])
            bot.reply_to(message, "Вы можете печатать или записывать голосовые сообщения только после вопроса.", reply_markup=keyboard)
    except Exception as e:
        bot.reply_to(message, "Произошла ошибка при обработке вашего ответа. Попробуйте снова.")
        print(f"Произошла ошибка: {e}")




# Запуск бота и расписания
if __name__ == '__main__':
    # Запуск потока для расписания
    schedule_thread = threading.Thread(target=run_schedule)
    schedule_thread.start()

    # Запуск бота
    bot.polling(none_stop=True)