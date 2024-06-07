import sqlite3
import random

def mark_questions_correct(user_id=5581286521, topic='Python', correct_date='2024-06-01'):
    # Connect to the database
    conn = sqlite3.connect('../trainingbot.db')
    cursor = conn.cursor()

    # Fetch all question_ids for the specified topic
    cursor.execute('''
        SELECT question_id FROM Questions WHERE question_topic = ?
    ''', (topic,))
    question_ids = cursor.fetchall()

    # Update each question for the specified user
    for question_id_tuple in question_ids:
        question_id = question_id_tuple[0]

        # Check if the answer already exists
        cursor.execute('''
            SELECT answer_id FROM Answers WHERE user_id = ? AND question_id = ?
        ''', (user_id, question_id))
        answer = cursor.fetchone()

        if answer:
            # Update the existing record
            cursor.execute('''
                UPDATE Answers
                SET is_correct = 1,
                    last_answer_date = ?,
                    last_correct_answer_date = ?,
                    number_of_correct_answers = number_of_correct_answers + 1,
                    number_of_attempts = number_of_attempts + 1
                WHERE user_id = ? AND question_id = ?
            ''', (correct_date, correct_date, user_id, question_id))
        else:
            # Insert a new record
            cursor.execute('''
                INSERT INTO Answers (user_id, question_id, is_correct, last_answer_date, last_correct_answer_date, number_of_correct_answers, number_of_attempts)
                VALUES (?, ?, 1, ?, ?, 1, 1)
            ''', (user_id, question_id, correct_date, correct_date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()
def mark_questions_skipped(user_id=5581286521, topic='GIL', skipped_date='2024-06-01'):
    # Connect to the database
    conn = sqlite3.connect('../trainingbot.db')
    cursor = conn.cursor()

    # Fetch all question_ids for the specified topic
    cursor.execute('''
        SELECT question_id FROM Questions WHERE question_topic = ?
    ''', (topic,))
    question_ids = cursor.fetchall()

    # Update each question for the specified user
    for question_id_tuple in question_ids:
        question_id = question_id_tuple[0]

        # Check if the answer already exists
        cursor.execute('''
            SELECT answer_id FROM Answers WHERE user_id = ? AND question_id = ?
        ''', (user_id, question_id))
        answer = cursor.fetchone()

        if answer:
            # Update the existing record
            cursor.execute('''
                UPDATE Answers
                SET number_of_times_skipped = number_of_times_skipped + 1,
                    last_skipped_day = ?
                WHERE user_id = ? AND question_id = ?
            ''', (skipped_date, user_id, question_id))
        else:
            # Insert a new record
            cursor.execute('''
                INSERT INTO Answers (user_id, question_id, number_of_times_skipped, last_skipped_day)
                VALUES (?, ?, 1, ?)
            ''', (user_id, question_id, skipped_date))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Call the functions to mark Python questions as correctly answered and 7 Frameworks questions as incorrectly answered
#mark_questions_correct()
mark_questions_skipped()