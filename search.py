# search.py
import requests

def search_books(query):
    url = f"https://openlibrary.org/search.json?q={query}"
    response = requests.get(url)
    data = response.json()
    results = []
    for book in data["docs"][:5]:
        results.append({
            "title": book.get("title", "Unknown"),
            "author": book.get("author_name", ["Unknown"])[0],
            "year": book.get("first_publish_year", 0)
        })
    return results