import sqlite3
import random

import openai
from openai import OpenAI
import telebot
from Backend import *

# OpenAI API key
client = OpenAI(api_key='sk-SeA46H6qerPo06VdVK2HxMabiqq7maWT',
                base_url="https://api.proxyapi.ru/openai/v1")


# Telegram bot token
bot = telebot.TeleBot("7088027566:AAE99kExngxUoqSZpjA3BngUNvA_72foolk")

MAX_MESSAGE_LENGTH = 4096  # Максимальная длина сообщения для Telegram

training_db = Training_db()
all_questions_with_answers = training_db.get_all_questions_with_answers()

# Ограничиваем длину ответов
#for question in all_questions_with_answers:
#    if len(all_questions_with_answers[question]) > MAX_MESSAGE_LENGTH:
#        all_questions_with_answers[question] = all_questions_with_answers[question][:MAX_MESSAGE_LENGTH]

question_list = list(all_questions_with_answers.items())
question_index = 0
statistics = []

# Печать первых 4 элементов словаря
first_four_items = list(all_questions_with_answers.items())[:4]
print("First four items in the dictionary:")
for key, value in first_four_items:
    print(f"Question: {key}\nAnswer: {value}\n")

# Function to get feedback from GPT-4
def get_feedback(question, user_response):
    prompt = f"""Действуй как опытный HR специалист, собеседующий кандидатов 
    на позицию джуниор по Python.
Ты задал вопрос: "{question}"
и принял ответ соискателя: "{user_response}".
Ты должен оценить ответ и дать обратную связь. Не будь слишком строгим, 
не отвергай ответ соискателя из-за грамматических ошибок, 
повторений или неверных указаний источников, так как это входная 
позиция в профессию. Если ответ включает в себя все главные пункты по вопросу, 
принимай его как правильный, но дополняй так,
 как ответил бы опытный программист по Python. 
 Начни ответ с 'Неправильный ответ' если ответ неправильный,
  и, пропустив строку, продолжи правильным ответом, 
  а далее кратким комментарием, почему ответ пользователя был 
  неправильным. Начни ответ с 'Правильный ответ' 
  если ответ правильный, и, пропустив строку, продолжи небольшими дополнениями до 
  идеального ответа от опытного программиста по Python. 
Твоя оценка должна иметь такую структуру:
- Правильный/неправильный ответ
- Правильный ответ (если ответ был неправильный)
- Комментарии по ответу."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "Ты опытный HR специалист."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Handler for the /start command
@bot.message_handler(commands=['start'])
def start(message):
    global question_index
    ask_next_question(message)

# Function to ask the next question and send it to GPT-4
def ask_next_question(message):
    global question_index
    if question_index < len(question_list):
        bot.send_message(message.chat.id, f'{question_index}')
        question, correct_answer = question_list[question_index]
        bot.send_message(message.chat.id, f"Вот ваш вопрос:\n{question}")

        # Send the correct answer to GPT-4
        feedback = get_feedback(question, correct_answer)

        # Determine the correctness of the feedback
        if feedback.startswith("Правильный ответ"):
            statistics.append(1)
        else:
            statistics.append(0)

        # Send feedback, limited to the maximum message length
        bot.send_message(message.chat.id, feedback[:MAX_MESSAGE_LENGTH])

        # Move to the next question
        question_index += 1
        ask_next_question(message)
    else:
        bot.send_message(message.chat.id, "Все вопросы заданы. Вот ваша статистика:")
        bot.send_message(message.chat.id,
                         f"Правильные ответы: {statistics.count(1)}\nНеправильные ответы: {statistics.count(0)}")

# Start polling
bot.polling()