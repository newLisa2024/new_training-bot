import telebot
from telebot import types
import telebot
from Backend import *
from db import *
from Backend import *


from datetime import datetime



start_message = (
    'Привет! 👋\n'
    'Добро пожаловать в нашего бота-тренажера для подготовки к собеседованию по Python!\n\n'
    'Здесь ты сможешь:\n'
    '📝 Отвечать на вопросы, чтобы проверить свои знания.\n'
    '📈 Следить за своим прогрессом и улучшать результаты.\n'
    '🤖 Получать полезный фидбэк на свои ответы.'
)
help_message = 'Здесь будет список доступных команд и описание их функций.'

# Словарь кнопок
buttons_dict = {
    'menu': 'На главную ↲',
    #'menu': '↺ ↴ ⤴ ⇗ ↗',
    'statistics': 'Статистика 📈',
    'test_mode': '❓ Тестирование',
    'back': 'Назад',
    'start_test': 'Начать тест',
    'all_questions': 'Все вопросы',
    'choose_topic': 'Выбрать тему',
    'see_answer_all': 'Узнать ответ👀',
    'next_question_all': '❓ Следующий',
    'detailed_statistics':'📑 Подробный',

    #'left': "⬅️",
    #'right': "➡️",
    'left': "⟵",
    'right': "⟶",
    #'left': '⬅',
    #'left': '◀',
    #'right': '▶',
    #'left': '⬅',
    #"right": "⇐",
    'text_report': '📑 Текстовый',
    'graph_report': 'Графический 📈',
    'skip_question_all': '❌ Пропустить',


    'repeat_topic': '↺ Повторить тему'
}

def add_topic_buttons(buttons_dict, list_of_topics):
    for idx, topic in enumerate(list_of_topics):
        button_key = f'topic_{idx}'
        buttons_dict[button_key] = topic


def create_see_answer_button(topic_index):
    return (f'see_answer_{topic_index}', '👀 Ответ')



# Функция для создания динамических кнопок пропуска вопросов по теме
def create_skip_question_button(topic_index):
    return (f'skip_question_{topic_index}', '❌ Пропустить')

def create_next_question_button(topic_index):
    return (f'next_question_{topic_index}', '❓ Следующий')


#при ошибке бот прекращает работу, а должен перезапускаться

#def error_handler(func):
#    def wrapper(*args, **kwargs):
#        try:
#            return func(*args, **kwargs)
#        except Exception as e:
#            print(f"Error in {func.__name__}: {e}")
#            message = kwargs.get('message') or args[0]
#            keyboard = create_inline_keyboard(['test_mode', 'statistics'])
#            bot.send_message(message.chat.id, "Произошла ошибка.", reply_markup=keyboard)
#    return wrapper

# Функция для создания inline клавиатуры


timer_message = "⏰ ⌛ Будет установлен таймер на 2 минуты.По истечении времени ответ будет засчитан. Вы можете пропустить вопрос, а также узнать на него правильный ответ, не отвечая. Если Вам понадобится больше времени, нажмите 'Еще 2 мин'\n Ответ Вы можете напечатать в поле ввода сообщения либо записать голосовым сообщением (говорите четко!)"















