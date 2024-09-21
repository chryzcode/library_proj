from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from book.models import *
from book.serializers import *
from user.serializers import *

@api_view(['POST'])
@permission_classes([IsAdminUser])
def add_book(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def remove_book(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Book.DoesNotExist:
        return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

        
@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_users_with_borrowed_books(request):
    users = User.objects.prefetch_related('borrowed_books').all()
    
    user_data = []
    for user in users:
        user_serialized = UserSerializer(user).data
        user_serialized['borrowed_books'] = BorrowBookSerializer(user.borrowed_books.all(), many=True).data
        user_data.append(user_serialized)
    
    return Response(user_data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_unavailable_books(request):
    books = Book.objects.filter(available=False)
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)