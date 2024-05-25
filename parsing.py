import sqlite3
import requests
from bs4 import BeautifulSoup
import logging


# Настройка логирования
logging.basicConfig(filename='parse_questions.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Создание таблицы Questions в базе данных trainingbot.db
def create_table():
    try:
        conn = sqlite3.connect('trainingbot.db')
        c = conn.cursor()

        # Создаем таблицу Questions
        c.execute('''
        CREATE TABLE IF NOT EXISTS Questions (
            question_id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_text TEXT NOT NULL,
            question_type TEXT NOT NULL,
            additional_text TEXT
        )
        ''')

        # Сохраняем изменения
        conn.commit()

    except sqlite3.Error as e:
        logging.error(f"Ошибка при создании таблицы: {e}")

    finally:
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
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logging.error(f"Ошибка при доступе к странице {url}: {e}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        question_links = soup.select(
            "a.link-offset-2.link-offset-3-hover.link-underline.link-underline-opacity-0.link-underline-opacity-75-hover[href*='/question/']")

        num_questions = len(question_links)
        total_questions += num_questions

        logging.info(f"Количество найденных вопросов на {url}: {num_questions}")

        for link in question_links:
            question_url = 'https://easyoffer.ru' + link['href']
            try:
                question_response = requests.get(question_url)
                question_response.raise_for_status()
                question_soup = BeautifulSoup(question_response.text, 'html.parser')
                question_text = question_soup.find('h1').text.strip()
                additional_text = None
                td_tag = question_soup.find('td', class_='d-none d-sm-table-cell')
                if td_tag:
                    additional_text = td_tag.text.strip()
                logging.info(f"Вопрос: {question_text}")
                if additional_text:
                    logging.info(f"Дополнительный текст: {additional_text}")

                c.execute('INSERT INTO Questions (question_text, question_type, additional_text) VALUES (?, ?, ?)',
                          (question_text, 'TEXT', additional_text))
                conn.commit()  # Фиксация транзакции после каждой успешной вставки

            except requests.RequestException as e:
                logging.error(f"Ошибка при доступе к странице вопроса {link['href']}: {e}")
            except sqlite3.Error as e:
                logging.error(f"Ошибка при вставке вопроса в базу данных: {e}")

    conn.close()

    logging.info(f"Общее количество найденных вопросов: {total_questions}")

# Вызов функции
create_table()
parse_questions()