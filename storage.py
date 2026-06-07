# storage.py
import sqlite3
from book import Book

def save_library(library):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books")
    for book in library:
        cursor.execute('''INSERT INTO books(title, author, year_published, read) VALUES (?, ?, ?, ?)''', (book.title, book.author, book.year_published, book.read))
    conn.commit()
    conn.close()

def load_library():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM books''')
    rows = cursor.fetchall()
    conn.close()
    return [Book.from_tuple(row) for row in rows]