import sqlite3


def get_mix_questions():
    # Подключение к базе данных
    conn = sqlite3.connect('../trainingbot.db')
    cursor = conn.cursor()

    # Запрос на получение всех вопросов по теме "Микс"
    cursor.execute('''
    SELECT question_id, question_text, question_answer
    FROM Questions
    WHERE question_topic = 'Микс'
    ''')

    # Извлечение всех результатов
    mix_questions = cursor.fetchall()

    # Закрытие соединения
    conn.close()

    return mix_questions

print(get_mix_questions())