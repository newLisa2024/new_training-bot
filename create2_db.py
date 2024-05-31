import sqlite3

# Подключаемся к базе данных (если файл базы данных не существует, он будет создан)
conn = sqlite3.connect('trbot.bd')
cursor = conn.cursor()

# Создаем таблицу Questions2
cursor.execute('''
CREATE TABLE Questions2 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_text TEXT NOT NULL,
    question_topic TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    question_type TEXT DEFAULT 'python'
)
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()

print("База данных и таблица Questions2 успешно созданы.")
