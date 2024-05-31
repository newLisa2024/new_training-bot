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
    conn = sqlite3.connect('trbot.bd')
    cursor = conn.cursor()
    cursor.execute('SELECT rowid, Question_text FROM Questions')
    questions = cursor.fetchall()
    if not questions:
        return None, "No questions available in the database."
    random_question = random.choice(questions)
    conn.close()
    return random_question[0], random_question[1]

# Function to get the correct answer from the database
def get_correct_answer(rowid):
    conn = sqlite3.connect('trbot.bd')
    cursor = conn.cursor()
    cursor.execute('SELECT Cquestion_answer FROM Questions WHERE rowid = ?', (rowid,))
    answer = cursor.fetchone()
    conn.close()
    return answer[0] if answer else "Answer not found."

# Function to send the question and user response to GPT-4 and get feedback
def get_feedback(question, user_response, correct_answer):
    prompt = f"""Действуй как опытный HR-программист, специалист по пайтону.
    Ты получил вопрос: "{question}"
    и ответ соискателя: "{user_response}".
    Вот правильный ответ: "{correct_answer}".
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
    rowid, question = get_random_question()
    if rowid is None:
        bot.send_message(message.chat.id, question)
        return
    bot.send_message(message.chat.id, f"Вот ваш вопрос:\n{question}\nПожалуйста, напишите ваш ответ.")
    bot.register_next_step_handler(message, handle_message, rowid, question)

# Handler for user responses
def handle_message(message, rowid, question):
    user_response = message.text
    correct_answer = get_correct_answer(rowid)  # Получение правильного ответа из базы данных
    feedback = get_feedback(question, user_response, correct_answer)
    bot.send_message(message.chat.id, feedback)

# Start polling
bot.polling()