import sqlite3
import random

def get_random_question():
    # Подключение к базе данных
    conn = sqlite3.connect('trainingbot.db')
    cursor = conn.cursor()

    # Получение всех ID вопросов
    cursor.execute('SELECT question_id FROM Questions')
    question_ids = cursor.fetchall()

    if not question_ids:
        return "No questions available in the database."

    # Выбор случайного ID вопроса
    random_id = random.choice(question_ids)[0]

    # Получение текста вопроса по случайному ID
    cursor.execute('SELECT question_text FROM Questions WHERE question_id = ?', (random_id,))
    question = cursor.fetchone()

    # Закрытие соединения
    conn.close()

    return question[0] if question else "Question not found."



