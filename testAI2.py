import sqlite3
import random
from openai import OpenAI
import telebot

# OpenAI API key
client = OpenAI(api_key='sk-SeA46H6qerPo06VdVK2HxMabiqq7maWT',
                base_url="https://api.proxyapi.ru/openai/v1")

# Telegram bot token
bot = telebot.TeleBot("6593004563:AAF6_VdpPQKQ-hYjsAcrz6GBwuVnx_CPwFc")

# Function to get a random question and its answer from the database
def get_random_question_and_answer():
    conn = sqlite3.connect('trbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT question_id FROM Questions')
    question_ids = cursor.fetchall()
    if not question_ids:
        return "Нет доступных вопросов в базе данных.", None
    while True:
        random_id = random.choice(question_ids)[0]
        cursor.execute('SELECT question_text, question_answer FROM Questions WHERE question_id = ?', (random_id,))
        question = cursor.fetchone()
        if question and question[1]:  # Ensure both question and answer are found
            conn.close()
            return question[0], question[1]
    conn.close()
    return "Вопрос не найден.", None

# Function to send the question and user response to GPT-4 and get feedback
def get_feedback(question, user_response):
    prompt = f"""Действуй как опытный HR.
    Ты получил вопрос: "{question}"
    и ответ соискателя: "{user_response}".
    Ты должен оценить ответ и дать обратную связь. Есть два варианта начала ответа : 'не правильный ответ' и 'правильный ответ'. "Правильный ответ" ты пишешь если ответ правильный, "не правильный ответ" ты пишешь если ответ неправильный или неполный. Если ответ не правильный, потом напиши правильный ответ. 
    Твоя оценка имеет такую структуру : Правильный/не правильный ответ , потом правильный ответ или , если ответ правильный маленькие добавления."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[
                {"role": "system", "content": "Ты опытный HR специалист."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Ошибка при запросе к OpenAI: {e}")
        return "Произошла ошибка при запросе к OpenAI."

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    question, answer = get_random_question_and_answer()
    if answer:
        feedback = get_feedback(question, answer)
        bot.send_message(message.chat.id, f"Вот ваш вопрос:\n{question}\nВот предложенный ответ:\n{answer}\nОценка:\n{feedback}")
    else:
        bot.send_message(message.chat.id, question)

# Start polling
bot.polling()
