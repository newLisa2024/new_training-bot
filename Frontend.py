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
    'test_mode': '❓Тестирование',
    'back': 'Назад',
    'start_test': 'Начать тест',
    'all_questions': 'Все вопросы',
    'choose_topic': 'Выбрать тему',
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
    'skip_question': '❌ Пропустить',
    'next_question': 'Следующий ⟶',
    'repeat_topic': '↺ Повторить тему'
}

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
@error_handler
def create_inline_keyboard(button_keys):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=buttons_dict[key], callback_data=key) for key in button_keys if key in buttons_dict]
    keyboard.add(*buttons)
    return keyboard

timer_message = "⏰ ⌛ Будет установлен таймер на 2 минуты.По истечении времени ответ будет засчитан."















