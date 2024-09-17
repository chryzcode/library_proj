from rest_framework import serializers
from .models import *
from user.serializers import UserSerializer

class BookSerializer(serializers.ModelSerializer):
     class Meta:
        model = Book
        fields = '__all__'


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BorrowBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowBook
        fields = ['id', 'user', 'book', 'duration_in_days', 'borrow_date', 'return_date']
        read_only_fields = ['user', 'book', 'borrow_date', 'return_date'] 