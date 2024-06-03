import sqlite3

# Функция для создания базы данных и таблиц
def init_database():
    # Подключение к базе данных (если файла не существует, он будет создан)
    conn = sqlite3.connect('trainingbot.db')
    # Включение поддержки внешних ключей
    conn.execute('PRAGMA foreign_keys = ON;')

    cursor = conn.cursor()

    # Создание таблицы Users
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
        user_id INTEGER PRIMARY KEY,
        registration_date TEXT NOT NULL,
        is_active INTEGER NOT NULL
    )
    ''')

    # Создание таблицы Questions
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT ,
        question_text TEXT NOT NULL,
        question_topic TEXT NOT NULL,
        question_type TEXT DEFAULT 'python',
        question_frequency INTEGER NOT NULL,
        question_answer TEXT 
    )
    ''')

    # Создание таблицы Answers
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Answers (
        answer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        question_id INTEGER NOT NULL,
        is_correct INTEGER,
        number_of_attempts INTEGER NOT NULL DEFAULT 0,
        last_answer_date TEXT NOT NULL,
        number_of_times_skipped INTEGER DEFAULT 0,
        last_skipped_day TEXT,
        last_correct_answer_date TEXT,
        number_of_correct_answers INTEGER DEFAULT 0,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (question_id) REFERENCES Questions(question_id),
        UNIQUE(user_id, question_id)
        
    )
    ''')

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

#init_database()