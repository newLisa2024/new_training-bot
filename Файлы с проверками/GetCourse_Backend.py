import sqlite3
class Getcourse:
    def __init__(self, db_path='getcourse.db'):
        self.db_path = db_path

    def _connect(self):
        # Этот метод используется для подключения к базе данных и обозначен как внутренний
        return sqlite3.connect(self.db_path)

    #Проверяет, соответствует ли параметр в ссылке параметру в базе ГК
    def check_parameter(self, param_text):
        conn = self._connect()  # Вызов внутреннего метода для подключения
        cursor = conn.cursor()
        cursor.execute('''
            SELECT is_active FROM parameters WHERE param_text = ?
        ''', (param_text,))
        result = cursor.fetchone()
        conn.close()
        if result is not None and result[0] == 1:
            return True
        return False

    #Проверяет, активен ли пользователь в базе ГК
    def check_user(self, user_id):
        conn = self._connect()  # Вызов внутреннего метода для подключения
        cursor = conn.cursor()
        cursor.execute('''
            SELECT is_active FROM getcourse_users WHERE user_id = ?
        ''', (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result is not None and result[0] == 1:
            return True
        return False