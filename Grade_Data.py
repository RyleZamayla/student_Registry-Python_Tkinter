import sqlite3


def Database():
    global conn, cursor
    conn = sqlite3.connect('db_Grade.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, student_no TEXT, student_name TEXT, course TEXT, subject TEXT, prelim TEXT, midterm TEXT, final TEXT, average TEXT, gpe TEXT, remarks TEXT)")

