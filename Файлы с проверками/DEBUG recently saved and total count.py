import sqlite3
def get_recent_questions(limit=10):
    conn = sqlite3.connect('../trainingbot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Questions ORDER BY question_id DESC LIMIT ?', (limit,))
    recent_questions = cursor.fetchall()

    conn.close()
    return recent_questions

recent_questions = get_recent_questions()
for question in recent_questions:
    print(question)

import sqlite3

def count_questions():
    conn = sqlite3.connect('../trainingbot.db')
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM Questions')
    count = cursor.fetchone()[0]

    conn.close()
    return count

total_questions = count_questions()
print(f"Total questions in the database: {total_questions}")