import time
from book import Book    
from storage import save_library, load_library
from search import search_books
from db import init_db

# Library
library = []

def display_menu():
    print("\nLibrary Menu:")
    print("1. View all books")
    print("2. Add a book")
    print("3. Mark a book as read")
    print("4. Mark a book as unread")
    print("5. Exit")

def display_books(book_list):
    if not book_list:
        print("No books in the library.")
    else:
        for i, book in enumerate(book_list):
            print(f"{i + 1}. {book.get_description()}")



init_db()
library = load_library()

print("\nWelcome to the Library!")

while True:
    time.sleep(1)
    display_menu()
    time.sleep(1.5)
    choice = input("Enter your choice (1-5): ")

    
# Handle user choices
    if choice == '1':
    # view all books
        print("\nHere's your books")
        display_books(library)
    elif choice == '2':
        query = input("Enter a search term: ")
        results = search_books(query)
        cancelled = False

        if not results:
            print("No results found.")
        else:
            for i, book in enumerate(results):
                print(f"{i + 1}. {book['title']} by {book['author']} ({book['year']})")
            
            while True:
                try:
                    pick = int(input("Enter the number of the book to add (0 to exit): ")) - 1
                    if pick == -1:
                        print("Cancelled adding a book.")
                        cancelled = True
                        break
                    elif 0 <= pick < len(results):
                        break
                    else:
                        print("Please enter a number from the list.")
                except ValueError:
                    print("Please enter a valid number.")
            
            if not cancelled:
                chosen = results[pick]
                new_book = Book(chosen["title"], chosen["author"], chosen["year"])
                library.append(new_book)
                print(f"'{chosen['title']}' has been added to the library.")
    elif choice == '3':
        # mark book as read
        unread = [book for book in library if not book.read]
        cancelled = False
        if not unread:
            print("You have read all your books! Time to pick something new.")
        else:
            display_books(unread)
            while True:
                try:
                    book_number = int(input("Enter the number of the book you've read (0 to exit): ")) - 1
                    if book_number == -1:
                        print("Cancelled marking a book as read.")
                        cancelled = True
                        break
                    if 0 <= book_number < len(unread):
                        break
                    else:                    
                        print("Please enter a number corresponding to a book in the library.")
                except ValueError:
                    print("Please enter a valid number.")
            if not cancelled:
                unread[book_number].read = True
                print("Marked as read.")

    elif choice == '4':
        # mark unread books as unread
        read_books = [book for book in library if book.read]
        cancelled = False
        if not read_books:
            print("You have no read books to mark as unread.")
        else:
            display_books(read_books)
            while True:
                try:
                    book_number = int(input("Enter the number of the book to mark as unread (0 to exit): ")) - 1
                    if book_number == -1:
                        print("Cancelled marking a book as unread.")
                        cancelled = True
                        break
                    if 0 <= book_number < len(read_books):
                        break
                    else:                    
                        print("Please enter a number corresponding to a book in the library.")
                except ValueError:
                    print("Please enter a valid number.")
            if not cancelled:
                read_books[book_number].read = False
                print("Marked as unread.")

    elif choice == '5':
        #exit
        save_library(library)
        print("Library saved. Goodbye!")
        break