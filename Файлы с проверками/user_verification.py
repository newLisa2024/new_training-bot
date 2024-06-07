import telebot
from config import BOT_TOKEN
from Getcourse_db import *

bot = telebot.TeleBot(BOT_TOKEN)

#init_getcourse_database()
#init_database()


#Тот случай, когда Параметры лежат в файле params.json
#def load_valid_codes():
#    with open('params.json', 'r') as file:
#        data = json.load(file)
#    return data['valid_codes']

#VALID_CODES = load_valid_codes()

#Тот случай, когда Параметры лежат в базе данных ГетКурса





@bot.message_handler(commands=['start'])
def start(message):
    try:
        verification_code = message.text.split()[1]
    except IndexError:
        bot.reply_to(message, "Введите код верификации после команды /start.")
        return

    access_level = VALID_CODES.get(verification_code)
    if access_level is not None:
        telegram_id = message.from_user.id
        bot.reply_to(message, f"Код верификации принят. Ваш уровень доступа: {access_level}. Ваши данные проверяются...")
        if check_user_in_external_db(telegram_id):
            bot.reply_to(message, "Вы успешно авторизованы!")
        else:
            bot.reply_to(message, "Ваши данные не найдены в базе данных.")
    else:
        bot.reply_to(message, "Введите правильный код верификации (4 символа, буквы и цифры).")

def check_user_in_external_db(telegram_id):
    # Заглушка проверки пользователя во внешней базе данных
    return True  # Всегда возвращаем True для MVP

def main():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    main()
