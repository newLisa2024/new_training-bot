import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('questions2.db')
cursor = conn.cursor()

# Получаем данные из 10-й строки таблицы questions2
cursor.execute('SELECT question, answer FROM questions2 LIMIT 1 OFFSET 9')
row = cursor.fetchone()

# Проверяем, что строка существует и выводим данные
if row:
    question, answer = row
    print(f"Вопрос в 10-й строке: {question}")
    print(f"Ответ в 10-й строке: {answer}")
else:
    print("10-я строка не найдена.")

# Закрываем соединение с базой данных
conn.close()
