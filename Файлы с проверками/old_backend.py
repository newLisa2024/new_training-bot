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

    # Функция для проверки, ответил ли пользователь на хотя бы один вопрос
        # Функция для проверки, ответил ли пользователь на хотя бы один вопрос
    def has_user_answered(self, user_id):
        self._connect()
        try:
            self.cursor.execute('''
            SELECT EXISTS(SELECT 1 FROM Answers WHERE user_id = ?)
            ''', (user_id,))
            result = self.cursor.fetchone()[0]
            return bool(result)
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            return False
        finally:
            self._close()

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

        # Функция для получения вопросов по теме

        #Алгоритм без Эббингауза
        # Функция для получения вопросов по теме
    #функция получает 15 вопросов с наивысшим шансом попадания их на интервью,
    # исключая те вопросы, на которые сегодня пользователь
    # ответил неверно или сегодня пропустил

    #def get_list_of_10_questions(self, user_id, question_topic):
    #    self._connect()

    #    try:
    #        # Получаем сегодняшнюю дату в формате YYYY-MM-DD
    #       today_date = datetime.now().strftime('%Y-%m-%d')

    #        # Определяем SQL-запрос в зависимости от темы
    #        if question_topic == 'all':
    #            query = '''
    #            SELECT q.question_text
    #            FROM Questions q
    #            LEFT JOIN Answers a ON q.question_id = a.question_id AND a.user_id = ?
    #            WHERE a.user_id IS NULL
    #            OR a.last_skipped_day != ?
    #            AND (a.is_correct != 0 AND a.last_answer_date != ?)
    #            ORDER BY q.question_frequency DESC
    #            LIMIT 10
    #            '''
    #            params = (user_id, today_date, today_date)
    #        else:
    #            query = '''
    #            SELECT q.question_text
    #            FROM Questions q
    #            LEFT JOIN Answers a ON q.question_id = a.question_id AND a.user_id = ?
    #            WHERE a.user_id IS NULL
    #            OR q.question_topic = ?
    #            AND a.last_skipped_day != ?
    #            AND (a.is_correct != 0 AND a.last_answer_date != ?)
    #            ORDER BY q.question_frequency DESC
    #            LIMIT 10
    #            '''
    #            params = (user_id, question_topic, today_date, today_date)

            # Выполняем запрос
    #        self.cursor.execute(query, params)

            # Получаем все подходящие вопросы
    #        questions = self.cursor.fetchall()

            # Преобразуем список кортежей в список строк (текстов вопросов)
    #        selected_questions = [q[0] for q in questions]

    #        return selected_questions

    #    except sqlite3.Error as e:
    #        print(f'Ошибка при работе с базой данных: {e}')
    #        return []

    #    finally:
    #        self._close()

    # Алгоритм с Эббингаузом
    # Функция для получения вопросов по теме
    # функция получает 15 вопросов с наивысшим шансом попадания их на интервью,
    # исключая те вопросы, на которые сегодня пользователь
    # ответил неверно или сегодня пропустил
    def get_list_of_10_questions(self, user_id, question_topic):
        self._connect()

        try:
            # Получаем сегодняшнюю дату в формате YYYY-MM-DD
            today_date = datetime.now().strftime('%Y-%m-%d')

            # Определяем SQL-запрос в зависимости от темы
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
                    today_date,
                    today_date, today_date
                )

            self.cursor.execute(query, params)
            questions = self.cursor.fetchall()
            return questions

        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            return []

        finally:
            self._close()

    def add_skipped_question(self, user_id, question_id, today_date):
        self._connect()
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
            self.cursor.execute(query, (user_id, question_id, today_date, today_date))
            self.conn.commit()
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
        finally:
            self._close()

        # Функция для получения правильного ответа на вопрос
    def get_correct_answer(self, question_id):
        self._connect()
        try:
            query = "SELECT question_answer FROM Questions WHERE question_id = ?"
            self.cursor.execute(query, (question_id,))
            result = self.cursor.fetchone()
            if result and result[0]:
                return result[0]
            else:
                return None
        except sqlite3.Error as e:
            print(f'Ошибка при работе с базой данных: {e}')
            return None
        finally:
            self._close()

    # Функция для получения даты последнего ответа
    def get_last_answer_date(self, user_id, topic=None):
        self._connect()
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

            self.cursor.execute(query, params)
            last_date = self.cursor.fetchone()[0]
            if last_date is None:
                last_date = "Никогда"
            return last_date
        finally:
            self._close()

    # Функция для получения количества правильных ответов за последние 7 и
    # если нужны 30 дней, ставим параметр days = 30
    def get_correct_answers_count_period(self, user_id, topic=None, days=7):
        self._connect()
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

            self.cursor.execute(query, params)
            count = self.cursor.fetchone()[0]
            return count
        finally:
            self._close()
#Получить список всех пользователей, которые не отвечали уже два дня и более
    def get_inactive_users(self):
        self._connect()
        query = """
        SELECT Answers.user_id, MAX(last_answer_date)
        FROM Answers
        JOIN Users ON Answers.user_id = Users.user_id
        WHERE Users.is_active = 1
        GROUP BY Answers.user_id
        HAVING MAX(last_answer_date) <= DATE('now', '-2 days')
        """
        self.cursor.execute(query)
        inactive_users = self.cursor.fetchall()
        self._close()
        return inactive_users

        # Функция для получения среднего количества попыток
    def get_average_attempts(self, user_id, topic=None):
        self._connect()
        try:
            if topic:
                query = '''
                SELECT AVG(number_of_attempts) 
                FROM Answers 
                JOIN Questions ON Answers.question_id = Questions.question_id 
                WHERE Answers.user_id = ? AND Questions.question_topic = ?
                '''
                params = (user_id, topic)
            else:
                query = '''
                SELECT AVG(number_of_attempts) 
                FROM Answers 
                WHERE user_id = ?
                '''
                params = (user_id,)

            self.cursor.execute(query, params)
            avg_attempts = self.cursor.fetchone()[0]
            if avg_attempts is None:
                avg_attempts = 0
            return round(avg_attempts)
        finally:
            self._close()

    #Cброс счетчиков при выборе повторить тему
    def reset_answers_for_user(self, user_id, topic=None):
        self._connect()
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
                self.cursor.execute(query, (today_date, user_id, topic))
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
                self.cursor.execute(query, (today_date, user_id))
            self.conn.commit()
        finally:
            self._close()


    def get_all_questions_with_answers(self):
        self._connect()
        query = '''
        SELECT question_text, question_answer
        FROM Questions
        WHERE question_answer IS NOT NULL
        '''
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        all_questions_with_answers = {row[0]: row[1] for row in rows}  # Swap key-value order
        self._close()
        return all_questions_with_answers

    def update_answer_record(self, user_id, question_id, feedback):
        self._connect()

        today_date = datetime.now().strftime('%Y-%m-%d')
        is_correct = 1 if feedback.startswith('Правильный') else 0

        if is_correct:
            self.cursor.execute("""
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
            self.cursor.execute("""
                INSERT INTO Answers (user_id, question_id, is_correct, number_of_attempts, last_answer_date)
                VALUES (?, ?, ?, 1, ?)
                ON CONFLICT(user_id, question_id) DO UPDATE SET
                    is_correct=excluded.is_correct,
                    number_of_attempts=Answers.number_of_attempts + 1,
                    last_answer_date=excluded.last_answer_date
            """, (user_id, question_id, is_correct, today_date))

        self.conn.commit()
        self._close()