# db

import psycopg2

def init_db():
    conn = psycopg2.connect(
        dbname='library',
        user='michaelgibbons',
        host="localhost"
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS books (
                        id SERIAL PRIMARY KEY,
                        title TEXT,
                        author TEXT,
                        year_published INTEGER,
                        read BOOLEAN DEFAULT FALSE
                    )
                   ''')
    conn.commit()
    conn.close()
