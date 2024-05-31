import requests
from bs4 import BeautifulSoup
import sqlite3
import logging
import time

# Configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler('parse_questions.log'),
        logging.StreamHandler()
    ]
)

# Function to create a database table
def create_table():
    try:
        conn = sqlite3.connect('trbot.db')
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS Questions (
                question_id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_text TEXT NOT NULL,
                question_topic TEXT NOT NULL,
                question_answer TEXT,
                question_type TEXT DEFAULT 'python'
            )
        ''')
        conn.commit()
        logging.info("Table Questions created or already exists.")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")
    finally:
        if conn:
            conn.close()

# Function to fetch question links
def fetch_question_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        question_links = soup.select(
            "a.link-offset-2.link-offset-3-hover.link-underline.link-underline-opacity-0.link-underline-opacity-75-hover[href*='/question/']")
        logging.info(f"Found {len(question_links)} question links on page {url}")
        return question_links
    except requests.RequestException as e:
        logging.error(f"Error accessing page {url}: {e}")
        return []

# Function to fetch question details
def fetch_question_details(question_url):
    for attempt in range(3):
        try:
            question_response = requests.get(question_url)
            question_response.raise_for_status()
            question_soup = BeautifulSoup(question_response.text, 'html.parser')
            question_text = question_soup.find('h1').text.strip()
            question_answer = question_soup.find('div', class_='card-body').text.strip() if question_soup.find('div', class_='card-body') else None
            question_topic = 'General'  # Default value

            topic_tag = question_soup.find('span', class_='topic-class')  # Assuming CSS class for topic
            if topic_tag:
                question_topic = topic_tag.text.strip()
            return question_text, question_topic, question_answer
        except requests.RequestException:
            logging.error(f"Error accessing question page {question_url}, attempt {attempt + 1}")
            time.sleep(5)
    return None, None, None

# Function to parse questions
def parse_questions():
    base_url = 'https://easyoffer.ru/rating/python_developer?page='
    urls = [f"{base_url}{i}" for i in range(1, 12)]  # Create a list of URLs from 1 to 11

    total_questions = 0

    try:
        conn = sqlite3.connect('trbot.db')
        c = conn.cursor()

        for url in urls:
            logging.info(f"Parsing page: {url}")
            question_links = fetch_question_links(url)
            num_questions = len(question_links)
            total_questions += num_questions
            logging.info(f"Number of questions found on {url}: {num_questions}")

            for link in question_links:
                question_url = 'https://easyoffer.ru' + link['href']
                logging.info(f"Parsing question: {question_url}")
                question_text, question_topic, question_answer = fetch_question_details(question_url)

                if question_text:
                    logging.info(f"Question2: {question_text}")
                    if question_answer:
                        logging.info(f"Answer: {question_answer}")

                    try:
                        c.execute('INSERT INTO Questions (question_text, question_type, question_topic, question_answer) VALUES (?, ?, ?, ?)',
                                  (question_text, 'python', question_topic, question_answer))
                        conn.commit()
                        logging.info(f"Question successfully inserted into the database.")
                    except sqlite3.Error as e:
                        logging.error(f"Error inserting question into database: {e}")

        logging.info(f"Total number of questions found: {total_questions}")

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

    finally:
        if conn:
            conn.close()

# Create the table and start parsing questions
create_table()
parse_questions()



