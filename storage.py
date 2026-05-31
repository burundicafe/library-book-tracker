# storage.py
import json
from book import Book

def save_library(library):
    with open("library.json", "w") as f:
        json.dump([book.to_dict() for book in library], f)

def load_library():
    with open("library.json", "r") as f:
        data = json.load(f)
        return [Book.from_dict(book_data) for book_data in data]