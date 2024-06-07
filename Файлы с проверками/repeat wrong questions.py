def repeat_wrong_and_skipped_questions(self, user_id, topic=None):
    conn = self._connect()
    cursor = conn.cursor()
    try:
        if topic:
            query = '''
            UPDATE Answers
            SET is_correct = NULL,
                last_skipped_day = NULL
                
            WHERE user_id = ? AND (is_correct = 0 OR is_correct IS NULL) 
            AND (question_id IN (
                SELECT question_id FROM Questions WHERE question_topic = ?
            ))
            '''
            cursor.execute(query, (user_id, topic))
        else:
            query = '''
            
            UPDATE Answers
            SET is_correct = NULL,
                last_skipped_day = NULL
                
            WHERE user_id = ? AND (is_correct = 0 OR is_correct IS NULL)
            '''
            cursor.execute(query, (user_id))
        conn.commit()
    finally:
        conn.close()




@bot.callback_query_handler(func=lambda call: call.data.startswith('repeat_wrong_and_skipped'))
@error_handler
def handle_repeat_wrong_and_skipped(call):
    user_id = call.from_user.id

    # Установить состояние пользователя
    current_questions = read_current_questions(user_id)
    current_questions["state"] = "None"
    write_current_questions(user_id, current_questions)

    data = call.data.split('_')
    if len(data) == 5 and data[4] == 'all':
        # Повтор всех вопросов

        tdb.repeat_wrong_and_skipped_questions(user_id)

        # Предлагаем пользователю начать тестирование или выбрать тему
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        test_button = types.InlineKeyboardButton(text='Все вопросы', callback_data='all_questions')
        choose_button = types.InlineKeyboardButton(text='Выбрать тему', callback_data='choose_topic')
        menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
        keyboard.add(choose_button, test_button, menu_button)
        bot.send_message(call.message.chat.id, 'Все неверные и пропущенные вопросы были сброшены. Вы можете начать заново.', reply_markup=keyboard)
    elif len(data) == 5:
        # Повтор вопросов по конкретной теме
        topic_index = int(data[4])
        topic_name = list_of_topics[topic_index]
        tdb.repeat_wrong_and_skipped_questions(user_id, topic_name)
        # Предлагаем пользователю начать тестирование или выбрать тему
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        test_button = types.InlineKeyboardButton(text='Все вопросы', callback_data='all_questions')
        choose_button = types.InlineKeyboardButton(text='Выбрать тему', callback_data='choose_topic')
        menu_button = types.InlineKeyboardButton(text='На главную ↲', callback_data='menu')
        keyboard.add(choose_button, test_button,  menu_button)
        bot.send_message(call.message.chat.id, f'Все неверные и пропущенные вопросы по теме "{topic_name}" были сброшены. Вы можете начать заново.', reply_markup=keyboard)


