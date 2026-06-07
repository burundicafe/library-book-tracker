# db

import sqlite3

def init_db():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT,
                        author TEXT,
                        year_published INTEGER,
                        read INTEGER DEFAULT 0
                    )
                   ''')
    conn.commit()
    conn.close()

init_db()