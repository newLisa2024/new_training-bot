import sqlite3
import random
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# OpenAI API key
openai.api_key = 'выш токен'


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


# Function to send the question and user response to GPT-4o and get feedback
async def get_feedback(question, user_response):
    prompt = f"""Действуй как опытный HR-программист, специалист по пайтону.
    Ты получил вопрос: "{question}"
    и ответ соискателя: "{user_response}".
    Ты должен оценить ответ и дать обратную связь. Твоя оценка должна начинаться с 'ответ правильный', если ответ правильный, или 'ответ не правильный', если ответ неправильный или неполный."""

    response = await openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Ты опытный HR специалист."},
            {"role": "user", "content": prompt}
        ]
    )
    print(response['choices'][0]['message']['content'])


# Asynchronous handler for the /start command
async def start(update: Update, context: CallbackContext):
    question = get_random_question()
    context.user_data['current_question'] = question
    await update.message.reply_text(f"Вот ваш вопрос:\n{question}\nПожалуйста, напишите ваш ответ.")


# Asynchronous handler for user responses
async def handle_message(update: Update, context: CallbackContext):
    user_response = update.message.text
    question = context.user_data.get('current_question', 'Вопрос не найден.')
    feedback = await get_feedback(question, user_response)
    await update.message.reply_text(feedback)


def main():
    # Telegram bot token
    application = Application.builder().token("ваш токен").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == '__main__':
    main()





