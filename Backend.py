from datetime import datetime
import sqlite3
import json
import os
import openai
from openai import OpenAI
from config import PROXY_API

# OpenAI API key
client = OpenAI(api_key=PROXY_API,
                base_url="https://api.proxyapi.ru/openai/v1")

class Training_db:
    def __init__(self, db_name='trainingbot.db'):
        self.db_name = db_name

    def _connect(self):
        conn = sqlite3.connect(self.db_name)
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn

    def add_user(self, user_id, registration_date=None):
        conn = self._connect()
        cursor = conn.cursor()
        if registration_date is None:
            registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            cursor.execute('''
            INSERT INTO Users (user_id, registration_date, is_active)
            VALUES (?, ?, ?)
            ''', (user_id, registration_date, 1))
            conn.commit()
            print(f'Пользователь {user_id} успешно добавлен в базу данных.')
        except sqlite3.IntegrityError:
            print(f'Пользователь {user_id} уже существует в базе данных.')
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
        finally:
            conn.close()

    def is_user_in_db(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        result = None
        try:
            cursor.execute('''
            SELECT is_active 
            FROM Users 
            WHERE user_id = ?
            ''', (user_id,))
            row = cursor.fetchone()
            if row is not None:
                result = row[0]
        finally:
            conn.close()
        return result

    def get_all_topics(self):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT DISTINCT question_topic 
            FROM Questions
            ''')
            unique_topics = [row[0] for row in cursor.fetchall()]
        finally:
            conn.close()
        return unique_topics

    def has_user_answered(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM Answers WHERE user_id = ?)
            ''', (user_id,))
            result = cursor.fetchone()[0]
            return bool(result)
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            return False
        finally:
            conn.close()

    def change_question_topics(self, old_topic='Нет', new_topic='Микс'):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            cursor.execute('''
            UPDATE Questions
            SET question_topic = ?
            WHERE question_topic = ?
            ''', (new_topic, old_topic))
            conn.commit()
        finally:
            conn.close()

    def get_correct_answers_count(self, user_id, topic):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            if topic.lower() == "all":
                query_correct = '''
                SELECT COUNT(*)
                FROM Answers AS A
                WHERE A.user_id = ? AND A.is_correct = 1
                '''
                query_total = '''
                SELECT COUNT(*)
                FROM Questions
                '''
                cursor.execute(query_correct, (user_id,))
                correct_answers_count = cursor.fetchone()[0]

                cursor.execute(query_total)
                total_questions_count = cursor.fetchone()[0]
            else:
                query_correct = '''
                SELECT COUNT(*)
                FROM Answers AS A
                JOIN Questions AS Q ON A.question_id = Q.question_id
                WHERE A.user_id = ? AND Q.question_topic = ? AND A.is_correct = 1
                '''
                query_total = '''
                SELECT COUNT(*)
                FROM Questions
                WHERE question_topic = ?
                '''
                cursor.execute(query_correct, (user_id, topic))
                correct_answers_count = cursor.fetchone()[0]

                cursor.execute(query_total, (topic,))
                total_questions_count = cursor.fetchone()[0]
        finally:
            conn.close()
        return correct_answers_count, total_questions_count

    def get_list_of_10_questions(self, user_id, question_topic):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            today_date = datetime.now().strftime('%Y-%m-%d')
            if question_topic == 'all':
                query = '''
                SELECT q.question_id, q.question_text
                FROM Questions q
                LEFT JOIN Answers a ON q.question_id = a.question_id AND a.user_id = ?
                WHERE a.user_id IS NULL
                    OR (
                        NOT (a.last_skipped_day = ?) 
                        AND NOT (a.is_correct = 0 AND  a.last_answer_date = ?)
                        AND ( 
                             a.is_correct = 1 
                             AND ( 
                                 (a.number_of_correct_answers = 1 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 1)
                                 OR (a.number_of_correct_answers = 2 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 6)
                                 OR (a.number_of_correct_answers = 3 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 24)
                                 OR (a.number_of_correct_answers = 4 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 36)
                                 OR (a.number_of_correct_answers = 5 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 84)
                                 OR (a.number_of_correct_answers = 6 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 210)
                             )                   
                        )
                    )
                ORDER BY q.question_frequency DESC
                LIMIT 10
                '''
                params = (
                    user_id, today_date, today_date, today_date, today_date, today_date, today_date, today_date,
                    today_date
                )
            else:
                query = '''
                SELECT q.question_id, q.question_text
                FROM Questions q
                LEFT JOIN Answers a ON q.question_id = a.question_id AND a.user_id = ?
                WHERE (a.user_id IS NULL AND q.question_topic = ?)
                    OR (
                       q.question_topic = ?
                       AND
                          (
                            NOT (a.last_skipped_day = ?) 
                            AND NOT (a.is_correct = 0 AND  a.last_answer_date = ?)
                            AND ( 
                                 a.is_correct = 1 
                                 AND ( 
                                     (a.number_of_correct_answers = 1 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 1)
                                     OR (a.number_of_correct_answers = 2 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 6)
                                     OR (a.number_of_correct_answers = 3 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 24)
                                     OR (a.number_of_correct_answers = 4 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 36)
                                     OR (a.number_of_correct_answers = 5 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 84)
                                     OR (a.number_of_correct_answers = 6 AND (julianday(?) - julianday(a.last_correct_answer_date)) >= 210)
                                 )                   
                            )
                          )
                       )   
                ORDER BY q.question_frequency DESC
                LIMIT 10
                '''
                params = (
                    user_id, question_topic, question_topic, today_date, today_date, today_date, today_date, today_date,
                    today_date, today_date, today_date
                )

            cursor.execute(query, params)
            questions = cursor.fetchall()
            return questions
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            return []
        finally:
            conn.close()

    def add_skipped_question(self, user_id, question_id, today_date):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            query = '''
            INSERT INTO Answers (user_id, question_id, number_of_attempts, last_skipped_day, number_of_times_skipped, last_answer_date)
            VALUES (?, ?, 1, ?, 1, ?)
            ON CONFLICT(user_id, question_id) DO UPDATE SET
            number_of_attempts = Answers.number_of_attempts + 1,
            last_skipped_day = excluded.last_skipped_day,
            number_of_times_skipped = Answers.number_of_times_skipped + 1,
            last_answer_date = excluded.last_answer_date
            '''
            cursor.execute(query, (user_id, question_id, today_date, today_date))
            conn.commit()
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
        finally:
            conn.close()

    def get_correct_answer(self, question_id):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            query = "SELECT question_answer FROM Questions WHERE question_id = ?"
            cursor.execute(query, (question_id,))
            result = cursor.fetchone()
            if result and result[0]:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            return None
        finally:
            conn.close()

    def get_last_answer_date(self, user_id, topic=None):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            if topic:
                query = '''
                SELECT MAX(last_answer_date) 
                FROM Answers 
                JOIN Questions ON Answers.question_id = Questions.question_id 
                WHERE Answers.user_id = ? AND Questions.question_topic = ?
                '''
                params = (user_id, topic)
            else:
                query = '''
                SELECT MAX(last_answer_date) 
                FROM Answers 
                WHERE user_id = ?
                '''
                params = (user_id,)

            cursor.execute(query, params)
            last_date = cursor.fetchone()[0]
            if last_date is None:
                last_date = "Никогда"
            return last_date
        finally:
            conn.close()

    def get_correct_answers_count_period(self, user_id, topic=None, days=7):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            if topic:
                query = '''
                SELECT COUNT(*)
                FROM Answers
                JOIN Questions ON Answers.question_id = Questions.question_id
                WHERE Answers.user_id = ? AND Questions.question_topic = ? 
                AND Answers.is_correct = 1 
                AND DATE(Answers.last_answer_date) >= DATE('now', ?)
                '''
                params = (user_id, topic, f'-{days} day')
            else:
                query = '''
                SELECT COUNT(*)
                FROM Answers
                WHERE user_id = ? 
                AND is_correct = 1 
                AND DATE(last_answer_date) >= DATE('now', ?)
                '''
                params = (user_id, f'-{days} day')

            cursor.execute(query, params)
            count = cursor.fetchone()[0]
            return count
        finally:
            conn.close()

    def get_inactive_users(self):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            query = """
            SELECT Answers.user_id, MAX(last_answer_date)
            FROM Answers
            JOIN Users ON Answers.user_id = Users.user_id
            WHERE Users.is_active = 1
            GROUP BY Answers.user_id
            HAVING MAX(last_answer_date) <= DATE('now', '-2 days')
            """
            cursor.execute(query)
            inactive_users = cursor.fetchall()
            return inactive_users
        finally:
            conn.close()

    def get_total_attempts(self,user_id, topic=None):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            query_week = '''
            SELECT SUM(number_of_attempts)
            FROM Answers
            JOIN Questions ON Answers.question_id = Questions.question_id
            WHERE Answers.user_id = ? AND DATE(Answers.last_answer_date) >= DATE('now', '-7 day')
            '''
            query_month = '''
            SELECT SUM(number_of_attempts)
            FROM Answers
            JOIN Questions ON Answers.question_id = Questions.question_id
            WHERE Answers.user_id = ? AND DATE(Answers.last_answer_date) >= DATE('now', '-30 day')
            '''

            params = [user_id]

            if topic:
                query_week += ' AND Questions.question_topic = ?'
                query_month += ' AND Questions.question_topic = ?'
                params.append(topic)

            cursor.execute(query_week, params)
            total_attempts_week = cursor.fetchone()[0]

            cursor.execute(query_month, params)
            total_attempts_month = cursor.fetchone()[0]

            # Handle cases where no attempts are found (return 0 instead of None)
            total_attempts_week = total_attempts_week if total_attempts_week else 0
            total_attempts_month = total_attempts_month if total_attempts_month else 0

        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            total_attempts_week = 0
            total_attempts_month = 0
        finally:
            conn.close()

        return total_attempts_week, total_attempts_month
    def get_average_attempts(self, user_id, topic=None):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            if topic:
                query = '''
                SELECT AVG(A.number_of_attempts) 
                FROM Answers A
                JOIN Questions Q ON A.question_id = Q.question_id 
                WHERE A.user_id = ? AND Q.question_topic = ? AND A.is_correct = 1
                '''
                params = (user_id, topic)
            else:
                query = '''
                SELECT AVG(number_of_attempts) 
                FROM Answers 
                WHERE user_id = ? AND is_correct = 1
                '''
                params = (user_id,)

            cursor.execute(query, params)
            avg_attempts = cursor.fetchone()[0]
            if avg_attempts is None:
                avg_attempts = 0
            return round(avg_attempts, 2)
        finally:
            conn.close()

    def reset_answers_for_user(self, user_id, topic=None):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            today_date = datetime.now().strftime('%Y-%m-%d')
            if topic:
                query = '''
                UPDATE Answers
                SET is_correct = 0,
                    number_of_attempts = 0,
                    last_answer_date = ?,
                    number_of_times_skipped = 0,
                    last_skipped_day = NULL,
                    last_correct_answer_date = NULL,
                    number_of_correct_answers = 0
                WHERE user_id = ? AND question_id IN (
                    SELECT question_id FROM Questions WHERE question_topic = ?
                )
                '''
                cursor.execute(query, (today_date, user_id, topic))
            else:
                query = '''
                UPDATE Answers
                SET is_correct = 0,
                    number_of_attempts = 0,
                    last_answer_date = ?,
                    number_of_times_skipped = 0,
                    last_skipped_day = NULL,
                    last_correct_answer_date = NULL,
                    number_of_correct_answers = 0
                WHERE user_id = ?
                '''
                cursor.execute(query, (today_date, user_id))
            conn.commit()
        finally:
            conn.close()

    def get_all_questions_with_answers(self):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            query = '''
            SELECT question_text, question_answer
            FROM Questions
            WHERE question_answer IS NOT NULL
            '''
            cursor.execute(query)
            rows = cursor.fetchall()
            all_questions_with_answers = {row[0]: row[1] for row in rows}
            return all_questions_with_answers
        finally:
            conn.close()

    def update_answer_record(self, user_id, question_id, feedback):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            today_date = datetime.now().strftime('%Y-%м-%д')
            is_correct = 1 if feedback.startswith('Правильный') else 0

            if is_correct:
                cursor.execute("""
                    INSERT INTO Answers (user_id, question_id, is_correct, number_of_attempts, last_answer_date, last_correct_answer_date, number_of_correct_answers)
                    VALUES (?, ?, ?, 1, ?, ?, 1)
                    ON CONFLICT(user_id, question_id) DO UPDATE SET
                        is_correct=excluded.is_correct,
                        number_of_attempts=Answers.number_of_attempts + 1,
                        last_answer_date=excluded.last_answer_date,
                        last_correct_answer_date=excluded.last_correct_answer_date,
                        number_of_correct_answers=Answers.number_of_correct_answers + 1
                """, (user_id, question_id, is_correct, today_date, today_date))
            else:
                cursor.execute("""
                    INSERT INTO Answers (user_id, question_id, is_correct, number_of_attempts, last_answer_date)
                    VALUES (?, ?, ?, 1, ?)
                    ON CONFLICT(user_id, question_id) DO UPDATE SET
                        is_correct=excluded.is_correct,
                        number_of_attempts=Answers.number_of_attempts + 1,
                        last_answer_date=excluded.last_answer_date
                """, (user_id, question_id, is_correct, today_date))

            conn.commit()
        finally:
            conn.close()



#GPT функции


#отправка к GPT на ответ, если пользователь попросил ответ, а в базе его нет
def ask_gpt(question_text):
    # Здесь будет логика для получения ответа от GPT
    return "Ответ от GPT (пока что заглушка)"



#функции для записи текущих вопросов пользователей в json current_questions{user_id}.json

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_json_filepath(user_id):
    directory = 'user_current_questions'
    ensure_directory_exists(directory)
    return os.path.join(directory, f'current_questions_{user_id}.json')

def read_current_questions(user_id):
    filepath = get_json_filepath(user_id)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if "questions" not in data:
                data["questions"] = {}
            if "timer_message_id" not in data:
                data["timer_message_id"] = None
            if "timer_start_time" not in data:
                data["timer_start_time"] = None
            if "state" not in data:
                data["state"] = "None"
            if "last_question_text" not in data:
                data["last_question_text"] = None
            print(f"Read data for user {user_id}: {data}")
            return data
    return {"questions": {}, "last_question_id": None, "last_question_text": None, "timer_message_id": None, "timer_start_time": None, "state": "None"}





def write_current_questions(user_id, data):
    filepath = get_json_filepath(user_id)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
        print(f"Wrote data for user {user_id}: {data}")


def remove_question_from_all_lists(user_id, question_id):
    current_questions = read_current_questions(user_id)

    # Удаление вопроса из списка всех вопросов
    all_key = f"all_{user_id}"
    if all_key in current_questions["questions"]:
        current_questions["questions"][all_key] = [q for q in current_questions["questions"][all_key] if
                                                   q[0] != question_id]

    # Удаление вопроса из всех других списков тем
    for key in current_questions["questions"]:
        if key != all_key:
            current_questions["questions"][key] = [q for q in current_questions["questions"][key] if
                                                   q[0] != question_id]

    write_current_questions(user_id, current_questions)

def clear_user_questions(user_id, topic_id=None):
    data = read_current_questions(user_id)
    if topic_id:
        key = f"{topic_id}_{user_id}"
    else:
        key = f"all_{user_id}"

    print(f"Trying to delete key: {key}")
    print(f"Current keys before deletion: {data['questions'].keys()}")

    if key in data["questions"]:
        del data["questions"][key]
        write_current_questions(user_id, data)
        print(f"Deleted key: {key}")
    else:
        print(f"Key not found: {key}")

    print(f"Current keys after deletion: {data['questions'].keys()}")


#REMINDER


# Функция для вычисления количества дней с последнего ответа
def days_since_last_answer(last_answer_date):
    last_date = datetime.strptime(last_answer_date, '%Y-%m-%d')
    days_diff = (datetime.now() - last_date).days
    return days_diff

# Функция для выбора правильного падежа слова "день"
def get_day_word(days):
    if days % 10 == 1 and days % 100 != 11:
        return "день"
    elif 2 <= days % 10 <= 4 and (days % 100 < 10 or days % 100 >= 20):
        return "дня"
    else:
        return "дней"


#Получение фидбэка от Чата

def get_feedback(question, user_response):
    prompt = f"""Действуй как опытный HR специалист, собеседующий кандидатов 
        на позицию джуниор по Python.
    Ты задал вопрос: "{question}"
    и принял ответ соискателя: "{user_response}".
    Ты должен оценить ответ и дать обратную связь. Ответы на вопросы ожидаются на 
    уровне требований к джуниор позиции. В комментарии дополняй ответы так,
     как ответил бы опытный программист по Python. 
     Начни ответ с 'Неправильный ответ' если ответ неправильный,
      и, пропустив строку, продолжи правильным ответом, 
      а далее кратким комментарием, почему ответ пользователя был 
      неправильным. Начни ответ с 'Правильный ответ' 
      если ответ правильный, и, пропустив строку, продолжи небольшими дополнениями до 
      идеального ответа от опытного программиста по Python. 
    Твоя оценка должна иметь такую структуру:
    - Правильный/неправильный ответ
    - Правильный ответ (если ответ был неправильный)
    - Комментарии по ответу."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "Ты опытный HR специалист."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

#если в базе ответов нет ответа, то создаем его по требованию
def question_answer_from_ChatGPT(question):
    prompt = f"""Ты опытный программист, специалист по Python.
    Вот вопрос для интервью на позицию программиста Python: "{question}".
    Ты должен ответить на этот вопрос, как если бы ты сам проходил интервью.
    Твой ответ должен быть полным и профессиональным."""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": "Ты опытный HR специалист."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content










