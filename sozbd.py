import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('questions2.db')
cursor = conn.cursor()

# Создание таблицы questions2, если она не существует
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    topic TEXT,
    answer TEXT
)
''')

conn.commit()
conn.close()
