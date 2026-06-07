# book.py

class Book:
    def __init__(self, title, author, year_published):
        self.title = title
        self.author = author
        self.year_published = year_published
        self.read = False

    def get_description(self):
        return f"{self.title} by {self.author} ({self.year_published}) - {'Read' if self.read else 'Unread'}"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "year_published": self.year_published,
            "read": self.read
        }
    @classmethod
    def from_dict(cls, data):
        book = cls(data["title"], data["author"], data["year_published"])
        book.read = data["read"]
        return book
    @classmethod
    def from_tuple(cls, row):
        book = cls(row[1], row[2], row[3])
        book.read = bool(row[4])
        return book
