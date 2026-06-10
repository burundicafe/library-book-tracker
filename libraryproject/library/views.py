from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer

@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

def index(request):
    books = Book.objects.all()
    return render(request, 'library/index.html', {'books': books})