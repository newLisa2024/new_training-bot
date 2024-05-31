import requests
from bs4 import BeautifulSoup
import sqlite3

# Определяем базовый URL и заголовки для запроса
base_url = "https://easyoffer.ru/rating/python_developer?page="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Создаем или подключаемся к базе данных SQLite
conn = sqlite3.connect('questions2.db')
cursor = conn.cursor()

# Создаем таблицу, если ее нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    topic TEXT,
    answer TEXT
)
''')


# Функция для обработки одной страницы
def process_page(page_number):
    url = base_url + str(page_number)
    print(f"Обработка страницы: {page_number}")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # Находим все строки таблицы
    rows = soup.select("table.table tbody tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) < 3:
            print("Недостаточное количество ячеек в строке, пропуск строки.")
            continue

        question_text_tag = cells[1].find("a")
        question_topic_tag = cells[2]
        answer_text_tag = cells[0]  # Изменили на cells[0], так как они должны содержать проценты.

        # Логируем сырое HTML строки для отладки
        print(f"HTML строки: {row}")

        if not question_text_tag or not question_topic_tag or not answer_text_tag:
            print(f"Один или несколько элементов не найдены, пропуск строки.")
            print(
                f"Найденные элементы: question_text_tag={question_text_tag}, question_topic_tag={question_topic_tag}, answer_text_tag={answer_text_tag}")
            continue

        # Извлекаем текст из тегов
        question_text = question_text_tag.text.strip() if question_text_tag else None
        question_topic = question_topic_tag.text.strip() if question_topic_tag else None
        answer_text = answer_text_tag.text.strip() if answer_text_tag else None

        print(f"Вопрос: {question_text}, Тема: {question_topic}, Ответ: {answer_text}")

        # Сохраняем данные в базу данных
        try:
            cursor.execute('''
            INSERT INTO questions (question, topic, answer) VALUES (?, ?, ?)
            ''', (question_text, question_topic, answer_text))
            conn.commit()
            print(f"Данные успешно сохранены: {question_text}, {question_topic}, {answer_text}")
        except sqlite3.Error as e:
            print(f"Ошибка при вставке данных: {e}")


# Обработка нескольких страниц
for page in range(1, 3):  # Настройте диапазон по мере необходимости
    process_page(page)

# Закрываем соединение с базой данных
conn.close()




