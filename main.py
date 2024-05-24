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


import sqlite3
import requests
from bs4 import BeautifulSoup
import openpyxl
import logging
import time

# Настройка логирования
logging.basicConfig(filename='parse_questions.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def create_excel_file():
    # Создаем новый файл Excel и добавляем лист
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Questions"
    # Добавляем заголовки столбцов
    ws.append(["ID", "Question Text", "Question Type", "Additional Text"])
    return wb, ws

def save_to_excel(ws, question_id, question_text, question_type, additional_text):
    # Добавляем строку с данными в лист
    ws.append([question_id, question_text, question_type, additional_text])

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
    question_id = 1

    wb, ws = create_excel_file()

    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            question_links = soup.select(
                "a.link-offset-2.link-offset-3-hover.link-underline.link-underline-opacity-0.link-underline-opacity-75-hover[href*='/question/']")

            num_questions = len(question_links)
            total_questions += num_questions

            logging.info(f"Количество найденных вопросов на {url}: {num_questions}")

            for link in question_links:
                question_url = 'https://easyoffer.ru' + link['href']
                for _ in range(3):  # Попробовать до 3 раз
                    question_response = requests.get(question_url)
                    if question_response.status_code == 200:
                        break
                    time.sleep(5)
                else:
                    logging.error(f"Ошибка при доступе к странице вопроса {link['href']}")
                    continue

                question_soup = BeautifulSoup(question_response.text, 'html.parser')
                question_text = question_soup.find('h1').text.strip()
                additional_text = None
                td_tag = question_soup.find('td', class_='d-none d-sm-table-cell')
                if (td_tag):
                    additional_text = td_tag.text.strip()
                logging.info(f"Вопрос: {question_text}")
                if (additional_text):
                    logging.info(f"Дополнительный текст: {additional_text}")

                save_to_excel(ws, question_id, question_text, 'TEXT', additional_text)
                question_id += 1
        else:
            logging.error(f"Ошибка при доступе к странице {url}")

    # Сохранение файла Excel
    wb.save("questions.xlsx")

    logging.info(f"Общее количество найденных вопросов: {total_questions}")

# Вызов функции
parse_questions()













