#from Backend import *
from datetime import datetime
import sqlite3




class Training_db:
    def __init__(self, db_name='trainingbot.db'):
        self.db_name = db_name

    def get_list_of_10_questions(self, user_id, question_topic):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()

            today_date = datetime.now().strftime('%Y-%m-%d')

            # Выполнение запроса без условий для проверки данных
            query = '''
                SELECT q.question_id, q.question_text
                FROM Questions q
                LEFT JOIN Answers a ON q.question_id = a.question_id AND a.user_id = ?
                WHERE q.question_topic = ?
                ORDER BY q.question_frequency DESC
                LIMIT 10
            '''
            params = (user_id, question_topic)

            print(f'Executing query with params: {params}')
            cursor.execute(query, params)
            questions = cursor.fetchall()
            print(f'Results without conditions: {questions}')

            if not questions:
                return []

            # Добавление условий по одному
            query_with_conditions = '''
                SELECT q.question_id, q.question_text
                FROM Questions q
                LEFT JOIN Answers a ON q.question_id = a.question_id AND a.user_id = ?
                WHERE q.question_topic = ?
                AND (a.last_skipped_day != ?)
                
                ORDER BY q.question_frequency DESC
                LIMIT 10
            '''
            params_with_conditions = (user_id, question_topic, today_date)

            print(f'Executing query with conditions with params: {params_with_conditions}')
            cursor.execute(query_with_conditions, params_with_conditions)
            questions_with_conditions = cursor.fetchall()
            print(f'Results with conditions: {questions_with_conditions}')

            return questions_with_conditions
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            return []
        finally:
            conn.close()

# Пример использования:
tdbase = Training_db()
questions = tdbase.get_list_of_10_questions(5581286521, 'Фреймворки')

print(questions)  # Выводим результат для проверки

#AND NOT (a.is_correct = 0 AND  a.last_answer_date = ?)
#                AND NOT (a.is_correct = 1))


print(questions)


def get_all_topic ():
    # Подключение к базе данных
    conn = sqlite3.connect('../trainingbot.db')
    cursor = conn.cursor()

    # Выполнение запроса и получение результатов
    cursor.execute('''
    SELECT a.*
    FROM Answers a
    JOIN Questions q ON a.question_id = q.question_id
    WHERE q.question_topic = ?
    ''', ('Фреймворки',))

    results = cursor.fetchall()



    return results

    # Закрытие соединения
    conn.close()

results = get_all_topic()
print(results)


# OR (
#                    q.question_topic = ?
#                    AND
#
#                         (NOT (a.last_skipped_day = ?)
#                          AND NOT (a.is_correct = 0 AND  a.last_answer_date = ?)
#                          AND NOT (a.is_correct = 1)))
#
#                         OR ( q.question_topic = ?#                         AND (
#                              NOT (a.last_skipped_day = ?)
#                              AND a.is_correct = 1
#                              AND (
#                                  (a.number_of_correct_answers = 1 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 1)
#                                  OR (a.number_of_correct_answers = 2 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 6)
#                                  OR (a.number_of_correct_answers = 3 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 24)
#                                  OR (a.number_of_correct_answers = 4 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 36)
#                                  OR (a.number_of_correct_answers = 5 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 84)
#                                  OR (a.number_of_correct_answers = 6 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 210)
#                              )
#                         )
#                       )

# params = (
#                 user_id, today_date, today_date, today_date, today_date, today_date, today_date, today_date,
#                 today_date, today_date
#             )
# params = (
#     user_id, question_topic, question_topic, today_date, today_date, question_topic, today_date, today_date,
#     today_date,
#     today_date, today_date, today_date, today_date
# )