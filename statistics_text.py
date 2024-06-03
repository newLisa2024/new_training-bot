from Backend import *
import pandas as pd


def format_table_with_lines(df):


    # Конвертация DataFrame в строку
    table_str = df.to_string(index=False).split('\n')
    # Создание строки с горизонтальными линиями
    line = '-' * max(len(row) for row in table_str)
    # Добавление горизонтальных линий между строками таблицы
    spaced_table_str = f'\n{line}\n'.join(table_str)
    return spaced_table_str

def get_progress(user_id, list_of_topics):
    statistics = {}

    # Статистика по темам
    topic_stats = {
        'Тема': [],
        'Всего вопросов': [],
        'Правильных ответов': [],
        'Прогресс': []
    }

    for topic in list_of_topics:
        correct_answers_count, total_questions_count = tdb.get_correct_answers_count(user_id, topic)
        statistics[topic] = (correct_answers_count, total_questions_count)
        topic_stats['Тема'].append(topic)
        topic_stats['Всего вопросов'].append(total_questions_count)
        topic_stats['Правильных ответов'].append(correct_answers_count)
        if total_questions_count > 0:
            progress = f'{correct_answers_count / total_questions_count * 100:.2f}%'
        else:
            progress = '0.00%'
        topic_stats['Прогресс'].append(progress)

    # Получение общей статистики по всем темам
    correct_answers_count_all, total_questions_count_all = tdb.get_correct_answers_count(user_id, "all")
    statistics["all"] = (correct_answers_count_all, total_questions_count_all)

    # Общая статистика
    overall_stats = {
        'Показатель': ['Всего вопросов', 'Правильных ответов', 'Прогресс'],
        'Значение': [total_questions_count_all, correct_answers_count_all, f'{correct_answers_count_all / total_questions_count_all * 100:.2f}%' if total_questions_count_all > 0 else '0.00%']
    }
    overall_df = pd.DataFrame(overall_stats)
    topics_df = pd.DataFrame(topic_stats)

    # Конвертация таблиц в текст с добавлением горизонтальных линий
    overall_table = format_table_with_lines(overall_df)
    topics_table = format_table_with_lines(topics_df)

    return overall_table, topics_table

