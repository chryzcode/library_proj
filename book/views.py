from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import *
from .serializers import *

@api_view(['GET'])
def available_books(request):
    books = Book.objects.filter(available=True)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_a_book(request, book_id):
    book = Book.objects.get(id=book_id)
    serializer = BookDetailSerializer(book)
    return Response(serializer.data)


#filter books by publishers
@api_view(['GET'])
def filter_books_by_publishers(request):
    pulisher_name = request.GET.get('publisher_name')
    books = Book.objects.filter(publisher=pulisher_name)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

# filter by category
@api_view(['GET'])
def filter_books_by_category(request):
    category_name = request.GET.get('category_name')
    books = Book.objects.filter(category__name=category_name)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def borrow_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        if not book.available:
            return Response({"error": "Book is not available for borrowing."}, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

    # Create the borrowing instance
    serializer = BorrowBookSerializer(data=request.data)
    
    if serializer.is_valid():
        # Save the borrow instance, setting the current user as the borrower
        serializer.save(user=request.user, book=book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)