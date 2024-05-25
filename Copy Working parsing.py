import requests
from bs4 import BeautifulSoup
import sqlite3


# Функция для сохранения вопроса в базу данных

def save_question(question_text, question_topic, question_type='python'):
    conn = sqlite3.connect('trainingbot.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO Questions (question_text, question_topic, question_type)
    VALUES (?, ?, ?)
    ''', (question_text, question_topic, question_type))

    conn.commit()
    conn.close()

# Функция для парсинга страницы и сохранения вопросов в базу данных
def parse_and_save_questions(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    for row in soup.select('tr'):
        question_text_tag = row.select_one('td:nth-of-type(2) a')
        question_topic_tag = row.select_one('td.d-none.d-sm-table-cell')

        if question_text_tag and question_topic_tag:
            question_text = question_text_tag.text.strip()
            question_topic = question_topic_tag.text.strip()
            save_question(question_text, question_topic)

# Функция для обработки нескольких страниц
def process_multiple_pages(base_url, start_page, end_page):
    for i in range(start_page, end_page + 1):
        url = f"{base_url}{i}"
        print(f"Processing page: {i}")
        parse_and_save_questions(url)

# URL для парсинга
base_url = 'https://easyoffer.ru/rating/python_developer?page='

# Парсинг нескольких страниц и сохранение вопросов в базу данных
process_multiple_pages(base_url, 1, 11)