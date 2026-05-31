book = {
    "title": "Our Reasonable Faith",
    "author": "Herman Bavinck",
    "year_published": 1956,
    "read": False
}

for key, value in book.items():
    print(f"{key}: {value}")

book["genre"] = "Theology"
print(book["genre"])

for key, value in book.items():
    print(f"{key}: {value}")

del book["genre"]
print(book)