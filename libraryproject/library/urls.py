from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/books/', views.book_list, name='book_list'),
    path('search/', views.search_books, name='search_books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('library/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book')
]