from django.urls import path
from .views import *

urlpatterns = [
    path("available_books/", available_books, name="available_books"),
    path("get_a_book/<int:book_id>/", get_a_book, name="get_a_book"),
    path("filter_books_by_publishers/", filter_books_by_publishers, name="filter_books_by_publishers"),
    path("filter_books_by_category/", filter_books_by_category, name="filter_books_by_category"),
]
