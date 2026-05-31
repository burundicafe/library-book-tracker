import time
import json
from book import Book    
from storage import save_library, load_library
from search import search_books

# Library
library = []

def display_menu():
    print("\nLibrary Menu:")
    print("1. Add a book")
    print("2. Mark a book as read")
    print("3. View all books")
    print("4. View unread books")
    print("5. Exit")

def display_books(book_list):
    if not book_list:
        print("No books in the library.")
    else:
        for i, book in enumerate(book_list):
            print(f"{i + 1}. {book.get_description()}")



try:
    library = load_library()
except FileNotFoundError:
    library = []

print("\nWelcome to the Library!")

while True:
    time.sleep(1)
    display_menu()
    time.sleep(1.5)
    choice = input("Enter your choice (1-5): ")

    
# Handle user choices
    if choice == '1':
        query = input("Enter a search term: ")
        results = search_books(query)

        if not results:
            print("No results found.")
        else:
            for i, book in enumerate(results):
                print(f"{i + 1}. {book['title']} by {book['author']} ({book['year']})")
            
            while True:
                try:
                    pick = int(input("Enter the number of the book to add: ")) - 1
                    if 0 <= pick < len(results):
                        break
                    else:
                        print("Please enter a number from the list.")
                except ValueError:
                    print("Please enter a valid number.")
            
            chosen = results[pick]
            new_book = Book(chosen["title"], chosen["author"], chosen["year"])
            library.append(new_book)
            print(f"'{chosen['title']}' has been added to the library.")
    elif choice == '2':
        # mark book as read
        display_books(library)
        while True:
            try:
                book_number = int(input("Enter the number of the book you've read: ")) - 1
                if 0 <= book_number < len(library):
                    break
                else:                    
                    print("Please enter a number corresponding to a book in the library.")
            except ValueError:
                print("Please enter a valid number.")
        library[book_number].read = True
        print("Marked as read.")
    elif choice == '3':
        # view all books
        print("\nHere's your books")
        display_books(library)
    elif choice == '4':
        # view unread books
        unread = [book for book in library if not book.read]
        display_books(unread)
    elif choice == '5':
        #exit
        save_library(library)
        print("Library saved. Goodbye!")
        break