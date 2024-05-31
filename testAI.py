import sqlite3
import random
from openai import OpenAI
import telebot

# OpenAI API key
client = OpenAI(api_key='sk-SeA46H6qerPo06VdVK2HxMabiqq7maWT',
                base_url="https://api.proxyapi.ru/openai/v1")


# Telegram bot token
bot = telebot.TeleBot("6593004563:AAF6_VdpPQKQ-hYjsAcrz6GBwuVnx_CPwFc")

# Function to get a random question from the database
def get_random_question():
    conn = sqlite3.connect('trainingbot.db')
    cursor = conn.cursor()
    cursor.execute('SELECT question_id FROM Questions')
    question_ids = cursor.fetchall()
    if not question_ids:
        return "No questions available in the database."
    random_id = random.choice(question_ids)[0]
    cursor.execute('SELECT Question_text FROM Questions WHERE question_id = ?', (random_id,))
    question = cursor.fetchone()
    conn.close()
    return question[0] if question else "Question not found."

# Function to send the question and user response to GPT-4 and get feedback
def get_feedback(question, user_response):
    prompt = f"""Действуй как опытный HR-программист, специалист по пайтону.
    Ты получил вопрос: "{question}"
    и ответ соискателя: "{user_response}".
    Ты должен оценить ответ и дать обратную связь. Есть два варианта начала ответа : 'правильный ответ', если ответ правильный, или 'не правильный ответ', если ответ неправильный или неполный. Если ответ не правильный, потом напиши правильный ответ. 
    Твоя оценка имеет такую структуру : Правильный/не правильный ответ , потом правильный ответ или , если ответ правильный маленькие добавления."""


    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        messages=[
            {"role": "system", "content": "Ты опытный HR специалист."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    question = get_random_question()
    bot.send_message(message.chat.id, f"Вот ваш вопрос:\n{question}\nПожалуйста, напишите ваш ответ.")
    bot.register_next_step_handler(message, handle_message, question)

# Handler for user responses
def handle_message(message, question):
    user_response = message.text
    feedback = get_feedback(question, user_response)
    bot.send_message(message.chat.id, feedback)

# Start polling
bot.polling()