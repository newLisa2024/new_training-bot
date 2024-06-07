import requests
from bs4 import BeautifulSoup
import sqlite3
import logging

# Настройка логирования
logging.basicConfig(filename='Файлы с проверками/parsing_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')


# Функция для создания базы данных и таблиц

# Функция для сохранения вопроса в базу данных
def save_question_to_db(conn, question_text, question_topic, question_frequency, question_answer):
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO Questions (question_text, question_topic, question_frequency, question_answer)
    VALUES (?, ?, ?, ?)
    ''', (question_text, question_topic, question_frequency, question_answer))
    conn.commit()


# Функция для получения вопросов со страницы
def get_questions_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    questions = []

    table_rows = soup.find_all('tr')
    for row in table_rows:
        cells = row.find_all('td')
        if len(cells) == 3:
            chance = cells[0].text.strip().replace('%', '')
            question_text = cells[1].text.strip()
            tag = cells[2].text.strip()
            question_link = row.find('a')['href']
            questions.append({"question": question_text, "tag": tag, "chance": chance, "link": question_link})

    return questions


# Функция для получения ответов со страницы вопроса
def get_answers_from_question_page(question_url):
    response = requests.get(question_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    answers = []

    card_bodies = soup.find_all('div', class_='card-body')
    for body in card_bodies:
        answer_paragraphs = body.find_all('p')
        answer_text = ' '.join([p.text for p in answer_paragraphs if p.text.strip()])
        if answer_text:
            answers.append(answer_text)

    return answers if answers else None


# Функция для получения всех вопросов с нескольких страниц
def get_all_questions(base_url, num_pages):
    all_questions = []
    for page in range(1, num_pages + 1):
        url = f"{base_url}?page={page}"
        questions = get_questions_from_page(url)
        all_questions.extend(questions)

    return all_questions


# Укажите базовый URL и количество страниц
base_url = "https://easyoffer.ru/rating/python_developer"
num_pages = 11

# Подключение к базе данных
conn = sqlite3.connect('trainingbot.db')

all_questions = get_all_questions(base_url, num_pages)

# Запись всех вопросов и ответов в базу данных с логированием
for page_num, question in enumerate(all_questions, start=1):
    question_url = f"https://easyoffer.ru{question['link']}"
    answers = get_answers_from_question_page(question_url)
    answers_text = ' | '.join(answers) if answers else None
    save_question_to_db(conn, question['question'], question['tag'], question['chance'], answers_text)

    log_message = f"Страница {page_num} Вопрос: {question['question']}, Тег: {question['tag']}, Шанс: {question['chance']}, Ответ: {answers_text}"
    logging.info(log_message)

# Закрытие подключения к базе данных
conn.close()
