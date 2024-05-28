import telebot

# Вставьте сюда ваш токен
API_TOKEN = 'YOUR_TOKEN_HERE'

bot = telebot.TeleBot(API_TOKEN)

# Обработчик для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'привет!')

# Обработчик для команды /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Это справочная информация по использованию бота.')

# Обработчик для команды /info
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, 'Этот бот создан для демонстрации ответов на команды.')

# Обработчик для команды /contact
@bot.message_handler(commands=['contact'])
def send_contact(message):
    bot.reply_to(message, 'Свяжитесь с нами по адресу email@example.com')

# Запуск бота
bot.polling()
