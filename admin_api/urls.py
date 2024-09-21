from django.urls import path
from .views import *


urlpatterns = [
    path("list_users/", list_users, name="list_users"),
    path("add_book/", add_book, name="add_book"),
    path("remove_book/<int:book_id>/", remove_book, name="remove_book"),
    path("list_users_with_borrowed_books/", list_users_with_borrowed_books, name="list_users_with_borrowed_books"),
    path("list_unavailable_books/", list_unavailable_books, name="list_unavailable_books"),
]