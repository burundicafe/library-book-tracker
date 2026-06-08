#app
from flask import Flask, jsonify, request
from storage import get_connection

app = Flask(__name__)

@app.route('/')
def running():
    data = request.get_json()

@app.route('/books', methods=['POST'])
def get_books():
    from book import Book

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    conn.close()

    books = [Book.from_tuple(row).to_dict() for row in rows]
    return jsonify(books)

def add_book():
    from book import Book

    data = request.get_json()
    title = data.get('title')
    author = data.get('author')
    year_published = data.get('year_published')

    if not title or not author or not year_published:
        return jsonify({"error": "Missing required fields"}), 400

    new_book = Book(title, author, year_published)

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, year_published, read) VALUES (%s, %s, %s, %s) RETURNING id",
        (new_book.title, new_book.author, new_book.year_published, new_book.read)
    )
    new_book_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({"message": "Book added successfully", "book_id": new_book_id}), 201

@app.route('/books/count')
def count_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({"count": count})

@app.route('/books/<int:book_id>')
def get_book(book_id):
    from book import Book

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        book = Book.from_tuple(row).to_dict()
        return jsonify(book)
    else:
        return jsonify({"error": "Book not found"}), 404