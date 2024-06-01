import sqlite3


def add_question_id():
    conn = sqlite3.connect('trbot.db')
    cursor = conn.cursor()

    # Добавление колонки question_id
    cursor.execute('ALTER TABLE Questions ADD COLUMN question_id INTEGER PRIMARY KEY AUTOINCREMENT')

    # Создание временной таблицы с новой структурой
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Questions_temp (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            question_topic TEXT NOT NULL,
            question_answer TEXT,
            question_type TEXT DEFAULT 'python'
        )
    ''')

    # Копирование данных из старой таблицы в новую
    cursor.execute('''
        INSERT INTO Questions_temp (question_text, question_topic, question_answer, question_type)
        SELECT question_text, question_topic, question_answer, question_type FROM Questions
    ''')

    # Удаление старой таблицы
    cursor.execute('DROP TABLE Questions')

    # Переименование временной таблицы в оригинальную
    cursor.execute('ALTER TABLE Questions_temp RENAME TO Questions')

    conn.commit()
    conn.close()


add_question_id()

