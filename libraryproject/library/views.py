import logging
import requests
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer

# Get the standard Python logger for Django error tracking
logger = logging.getLogger(__name__)


@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


def index(request):
    # Retrieve all books, ordered by title for consistent pagination
    book_list = Book.objects.all().order_by('title') 
    
    # Set up the Paginator to show 10 items per page
    paginator = Paginator(book_list, 10) 
    
    # Get the current page number from the URL
    page_number = request.GET.get('page')
    
    # Generate the page object
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'library/index.html', {'page_obj': page_obj})


def search_books(request):
    results = []
    query = request.GET.get('q', '').strip()

    # Ensure limit is a valid integer and clamped to Google's max (40)
    try:
        limit = min(int(request.GET.get('limit', 5)), 40)
    except ValueError:
        limit = 5

    if query:
        url = "https://www.googleapis.com/books/v1/volumes"

        payload = {
            'q': query,
            'maxResults': limit,
            'key': settings.GOOGLE_API_KEY
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, params=payload, headers=headers, timeout=5)
            response.raise_for_status()
            data = response.json()

            for item in data.get('items', []):
                volume_info = item.get('volumeInfo', {})
                authors = volume_info.get('authors', [])

                # Extract and clean the year safely
                raw_date = volume_info.get('publishedDate', '')
                year = raw_date.split('-')[0] if raw_date else '—'

                results.append({
                    "title": volume_info.get('title', 'Unknown Title'),
                    "author": authors[0] if authors else "Unknown Author",
                    "year": year,
                    "publisher": volume_info.get('publisher', 'Unknown Publisher')
                })

        except requests.exceptions.RequestException as e:
            logger.error(f"Google Books API request failed: {e}")

    return render(request, 'library/search.html', {
        'results': results,
        'query': query,
        'limit': limit
    })


@require_POST
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        notes = request.POST.get('notes', '')
        publisher = request.POST.get('publisher')
        year_published = request.POST.get('year_published')

        try:
            year_published = int(year_published)
        except (ValueError, TypeError):
            year_published = 0  

        # 1. Identify if the request is coming from our JavaScript fetch
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        # 2. Check for duplicates
        if Book.objects.filter(title=title, author=author).exists():
            msg = f'"{title}" is already in your library.'
            if is_ajax:
                return JsonResponse({'status': 'warning', 'message': msg})
            
            # Fallback if JavaScript fails
            messages.warning(request, msg)
            return redirect('index')

        # 3. Create the new book
        Book.objects.create(
            title=title,
            author=author,
            notes=notes,
            publisher=publisher,
            year_published=year_published,
            read=False 
        )
        
        msg = f'"{title}" has been added to your library!'
        if is_ajax:
            return JsonResponse({'status': 'success', 'message': msg})

        # Fallback if JavaScript fails
        messages.success(request, msg)
        return redirect('index')


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.notes = request.POST.get('notes', '')  # Update notes field
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