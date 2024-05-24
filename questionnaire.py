import sqlite3
import requests
from bs4 import BeautifulSoup
import logging
import time

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler('parse_questions.log'),
        logging.StreamHandler()
    ]
)
def create_table():
    try:
        conn = sqlite3.connect('trainingbot.db')
        c = conn.cursor()
        # Создаем таблицу Questions
        c.execute('''
            CREATE TABLE IF NOT EXISTS Questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                question_topic TEXT NOT NULL,
                question_type TEXT DEFAULT 'python'
            )
        ''')
        conn.commit()
        logging.info("Таблица Questions создана или уже существует.")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при создании таблицы: {e}")
    finally:
        if conn:
            conn.close()

def fetch_question_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        question_links = soup.select(
            "a.link-offset-2.link-offset-3-hover.link-underline.link-underline-opacity-0.link-underline-opacity-75-hover[href*='/question/']")
        logging.info(f"Найдено {len(question_links)} ссылок на вопросы на странице {url}")
        return question_links
    except requests.RequestException as e:
        logging.error(f"Ошибка при доступе к странице {url}: {e}")
        return []

def fetch_question_details(question_url):
    for attempt in range(3):
        try:
            question_response = requests.get(question_url)
            question_response.raise_for_status()
            question_soup = BeautifulSoup(question_response.text, 'html.parser')
            question_text = question_soup.find('h1').text.strip()
            additional_text = None
            question_topic = 'General'  # Значение по умолчанию

            topic_tag = question_soup.find('span', class_='topic-class')  # Предполагаемый CSS-класс для темы
            if topic_tag:
                question_topic = topic_tag.text.strip()

            td_tag = question_soup.find('td', class_='d-none d-sm-table-cell')
            if (td_tag):
                additional_text = td_tag.text.strip()
            return question_text, question_topic, additional_text
        except requests.RequestException:
            logging.error(f"Ошибка при доступе к странице вопроса {question_url}, попытка {attempt + 1}")
            time.sleep(5)
    return None, None, None

def parse_questions():
    base_url = 'https://easyoffer.ru/rating/python_developer?page='
    urls = [f"{base_url}{i}" for i in range(1, 12)]  # Создаем список ссылок с 1 по 11

    total_questions = 0

    try:
        conn = sqlite3.connect('trainingbot.db')
        c = conn.cursor()

        for url in urls:
            logging.info(f"Парсинг страницы: {url}")
            question_links = fetch_question_links(url)
            num_questions = len(question_links)
            total_questions += num_questions
            logging.info(f"Количество найденных вопросов на {url}: {num_questions}")

            for link in question_links:
                question_url = 'https://easyoffer.ru' + link['href']
                logging.info(f"Парсинг вопроса: {question_url}")
                question_text, question_topic, additional_text = fetch_question_details(question_url)

                if question_text:
                    logging.info(f"Вопрос: {question_text}")
                    if additional_text:
                        logging.info(f"Дополнительный текст: {additional_text}")

                    try:
                        c.execute('INSERT INTO Questions (question_text, question_type, question_topic) VALUES (?, ?, ?)',
                                  (question_text, 'python', question_topic))
                        conn.commit()
                        logging.info(f"Вопрос успешно вставлен в базу данных.")
                    except sqlite3.Error as e:
                        logging.error(f"Ошибка при вставке вопроса в базу данных: {e}")

        logging.info(f"Общее количество найденных вопросов: {total_questions}")

    except sqlite3.Error as e:
        logging.error(f"Ошибка при работе с базой данных: {e}")

    finally:
        if conn:
            conn.close()

create_table()
parse_questions()


