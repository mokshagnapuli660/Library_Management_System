import sqlite3

connection = sqlite3.connect("library.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    category TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS issued_books(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    book_id INTEGER,
    issue_date TEXT
)
""")

connection.commit()
connection.close()

print("Database Created Successfully!")