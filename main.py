import sqlite3
import requests
from bs4 import BeautifulSoup


#TOKEN = 'YOUR_BOT_TOKEN'
#bot = telebot.TeleBot(TOKEN)

# Создание таблицы Questions в базе данных trainingbot.db
try:
    conn = sqlite3.connect('trainingbot.db')
    c = conn.cursor()

    # Создаем таблицу Questions
    c.execute('''
    CREATE TABLE IF NOT EXISTS Questions (
        question_id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        question_type TEXT NOT NULL
    )
    ''')

    # Сохраняем изменения
    conn.commit()

except sqlite3.Error as e:
    print(f"Ошибка при создании таблицы: {e}")

finally:
    # Закрываем соединение с базой данных
    if conn:
        conn.close()


def parse_questions():
    urls = [
        'https://easyoffer.ru/rating/python_developer',
        'https://easyoffer.ru/rating/python_developer?page=2',
        'https://easyoffer.ru/rating/python_developer?page=3',
        'https://easyoffer.ru/rating/python_developer?page=4',
        'https://easyoffer.ru/rating/python_developer?page=5',
        'https://easyoffer.ru/rating/python_developer?page=6',
        'https://easyoffer.ru/rating/python_developer?page=7',
        'https://easyoffer.ru/rating/python_developer?page=8',
        'https://easyoffer.ru/rating/python_developer?page=9',
        'https://easyoffer.ru/rating/python_developer?page=10',
        'https://easyoffer.ru/rating/python_developer?page=11',
    ]

    total_questions = 0

    conn = sqlite3.connect('trainingbot.db')
    c = conn.cursor()

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Находим все элементы по заданному CSS-селектору
            question_links = soup.select(
                "a.link-offset-2.link-offset-3-hover.link-underline.link-underline-opacity-0.link-underline-opacity-75-hover[href*='/question/']")

            # Подсчет количества вопросов на текущей странице
            num_questions = len(question_links)
            total_questions += num_questions

            print(f"Количество найденных вопросов на {url}: {num_questions}")

            # Переход по каждой ссылке и вывод текста вопроса
            for link in question_links:
                question_url = 'https://easyoffer.ru' + link['href']
                question_response = requests.get(question_url)
                if question_response.status_code == 200:
                    question_soup = BeautifulSoup(question_response.text, 'html.parser')
                    # Предположим, что текст вопроса находится в теге <h1>
                    question_text = question_soup.find('h1').text.strip()
                    print(question_text)

                    # Сохранение вопроса в базу данных
                    try:
                        c.execute('INSERT INTO Questions (question_text, question_type) VALUES (?, ?)',
                                  (question_text, 'TEXT'))
                    except sqlite3.Error as e:
                        print(f"Ошибка при вставке вопроса в базу данных: {e}")
                else:
                    print(f"Ошибка при доступе к странице вопроса {link['href']}")
        else:
            print(f"Ошибка при доступе к странице {url}")

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()

    print(f"Общее количество найденных вопросов: {total_questions}")


# Вызов функции
parse_questions()












