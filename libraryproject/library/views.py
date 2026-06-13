import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .serializers import BookSerializer
from django.contrib import messages
from django.shortcuts import redirect
from django.views.decorators.http import require_POST



@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

def index(request):
    books = Book.objects.all()
    return render(request, 'library/index.html', {'books': books})

import requests
from django.shortcuts import render

def search_books(request):
    results = []
    query = request.GET.get('q', '').strip()
    limit = int(request.GET.get('limit', 5))

    if query:
        # Google Books Volumes Search Endpoint
        url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={limit}"
        
        try:
            response = requests.get(url)
            data = response.json()
            
            # Google Books returns records inside an array called 'items'
            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                
                # Google returns authors as a list array
                authors = volume_info.get('authors', [])
                
                # Setup fallbacks for missing pieces
                title = volume_info.get('title', 'Unknown Title')
                primary_author = authors[0] if authors else "Unknown Author"
                publisher = volume_info.get('publisher', 'Unknown Publisher')
                
                # Google Books dates are formatted as YYYY-MM-DD; this clips out just the year
                raw_date = volume_info.get('publishedDate', '—')
                year = raw_date.split('-')[0] if raw_date != '—' else '—'
                
                # Look for secondary contributor markers if available in the description snippet
                description = volume_info.get('description', '')
                translator_clean = ""
                
                # If there are multiple authors listed, the second one is often the translator/editor
                if len(authors) > 1:
                    translator_clean = authors[1]

                results.append({
                    "title": title,
                    "author": primary_author,
                    "year": year,
                    "publisher": publisher,
                    "translator": translator_clean
                })
                
        except requests.exceptions.RequestException:
            pass

    return render(request, 'library/search.html', {
        'results': results,
        'query': query,
        'limit': limit
    })

@require_POST
def add_book(request):
    """Processes the form data submitted from a table row click and creates a new book."""
    title = request.POST.get('title')
    author = request.POST.get('author')
    translator = request.POST.get('translator', '')
    publisher = request.POST.get('publisher')
    year_published = request.POST.get('year_published')


    # Fallback to prevent crashes if year is missing or improperly formatted
    try:
        year_published = int(year_published)
    except (ValueError, TypeError):
        year_published = 0  

    # Save to your local Django database model
    Book.objects.create(
        title=title,
        author=author,
        translator=translator,
        publisher=publisher,
        year_published=year_published,
        read=False  # Defaulting new additions to Unread
    )

    # Redirect straight back to your main library dashboard index view
    return redirect('index')

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.translator = request.POST.get('translator') # <-- Save adjustments
        book.publisher = request.POST.get('publisher')
        book.year_published = request.POST.get('year_published')
        book.read = 'read' in request.POST
        book.save()
        return redirect('index')
    return render(request, 'library/book_detail.html', {'book': book})

@require_POST
def delete_book(request, pk):
    """Locates a local library book by its primary key and deletes it."""
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect('index')