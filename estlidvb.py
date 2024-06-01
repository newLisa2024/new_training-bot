import sqlite3


def count_remaining_rows():
    conn = sqlite3.connect('trbot.db')
    cursor = conn.cursor()

    # Подсчет количества оставшихся строк в таблице
    cursor.execute("SELECT COUNT(*) FROM Questions")
    count = cursor.fetchone()[0]

    conn.close()
    return count


remaining_rows = count_remaining_rows()
print(f"Количество оставшихся строк в таблице: {remaining_rows}")





