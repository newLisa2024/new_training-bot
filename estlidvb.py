import sqlite3
import logging

# Configuration for logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    handlers=[
        logging.FileHandler('fetch_answers.log'),
        logging.StreamHandler()
    ]
)


def fetch_answers(start_id, end_id):
    try:
        conn = sqlite3.connect('trbot.db')
        c = conn.cursor()
        c.execute('SELECT question_id, question_text, question_answer FROM Questions WHERE question_id BETWEEN ? AND ?',
                  (start_id, end_id))
        rows = c.fetchall()

        if rows:
            for row in rows:
                logging.info(f"Row {row[0]}: {row[1]} - {row[2]}")
        else:
            logging.info(f"No rows found between {start_id} and {end_id}.")

        return rows

    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

    finally:
        if conn:
            conn.close()


# Fetch answers from 10th to 29th row
rows = fetch_answers(10, 29)
for row in rows:
    print(f"Row {row[0]}: {row[1]} - {row[2]}")

