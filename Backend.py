from datetime import datetime
import sqlite3


class Training_db:
    def __init__(self, db_name='trainingbot.db'):
        self.db_name = db_name

    def _connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.conn.execute('PRAGMA foreign_keys = ON;')
        self.cursor = self.conn.cursor()

    def _close(self):
        if self.conn:
            self.conn.close()



    # Функция для добавления пользователя в базу данных
    def add_user(self, user_id, registration_date=None):
        self._connect()
        if registration_date is None:
            registration_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        try:
            # Попытка добавить нового пользователя
            self.cursor.execute('''
            INSERT INTO Users (user_id, registration_date, is_active)
            VALUES (?, ?, ?)
            ''', (user_id, registration_date, 1))
            self.conn.commit()
            print(f'Пользователь {user_id} успешно добавлен в базу данных.')

        except sqlite3.IntegrityError:
            # Ошибка вставки возникает, если пользователь уже существует
            print(f'Пользователь {user_id} уже существует в базе данных.')

        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')

        finally:
            self._close()
    # Функция, которая проверяет, есть ли пользователь
    # в базе данных и активен ли он (возвращает 1 или 0 - активен или нет
    # либо None, если пользователь не найден.)
    def is_user_in_db(self, user_id):
        self._connect()
        result = None
        try:
            self.cursor.execute('''
            SELECT is_active 
            FROM Users 
            WHERE user_id = ?
            ''', (user_id,))
            row = self.cursor.fetchone()
            if row is not None:
                result = row[0]
        finally:
            self._close()
        return result

    # Функция, которая возвращает все уникальные темы вопросов
    def get_all_topics(self):
        self._connect()

        try:
            # Запрос для получения уникальных тем вопросов
            self.cursor.execute('''
            SELECT DISTINCT question_topic 
            FROM Questions
            ''')

            # Получение всех уникальных тем
            unique_topics = [row[0] for row in self.cursor.fetchall()]
        finally:
            # Закрытие соединения
            self._close()

        return unique_topics

    # Функция, которая меня ет раздел Нет на раздел Микс,
    # просто для лучшего восприятия пользователем
    def change_question_topics(self, old_topic='Нет', new_topic='Микс'):
        self._connect()

        try:
            # Обновление тем вопросов
            self.cursor.execute('''
            UPDATE Questions
            SET question_topic = ?
            WHERE question_topic = ?
            ''', (new_topic, old_topic))

            self.conn.commit()
        finally:
            # Закрытие соединения
            self._close()

    #Функция для получения кортежа (количества верных ответов пользователя
    #по темам. В случае, когда надо получить верные ответы по всем
    #темам вопросов, параметр topic = "all", общее количество вопросов по теме или в базе,
    # если topic = "all")
    def get_correct_answers_count(self, user_id, topic):
        self._connect()
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
                self.cursor.execute(query_correct, (user_id,))
                correct_answers_count = self.cursor.fetchone()[0]

                self.cursor.execute(query_total)
                total_questions_count = self.cursor.fetchone()[0]
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
                self.cursor.execute(query_correct, (user_id, topic))
                correct_answers_count = self.cursor.fetchone()[0]

                self.cursor.execute(query_total, (topic,))
                total_questions_count = self.cursor.fetchone()[0]
        finally:
            self._close()
        return correct_answers_count, total_questions_count