# storage.py
import psycopg2
from book import Book

def get_connection():
    return psycopg2.connect(
        dbname='library',
        user='michaelgibbons',
        host="localhost"
    )

def save_library(library):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books")
    for book in library:
        cursor.execute('''INSERT INTO books(title, author, year_published, read) VALUES (%s, %s, %s, %s)''', (book.title, book.author, book.year_published, book.read))
    conn.commit()
    conn.close()

def load_library():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()
    return [Book.from_tuple(row) for row in rows]