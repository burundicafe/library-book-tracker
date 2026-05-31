import requests

response = requests.get("https://openlibrary.org/search.json?q=herman+bavinck")
data = response.json()

print(data["numFound"])

first_book = data["docs"][0]
for book in data["docs"][:5]:
    print(f"{book['title']} by {book.get('author_name', ['Unknown'])[0]} ({book.get('first_publish_year', 'Unknown')})")