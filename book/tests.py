from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Book, Category, BorrowBook

User = get_user_model()

class BookTests(APITestCase):
    def setUp(self):
        # Create a test user who will login with an email
        self.user = User.objects.create_user(email='testuser@example.com', password='testpass')

        # Create sample publisher and category
      
        self.category = Category.objects.create(name='Test Category')

        # Create sample books
        self.book1 = Book.objects.create(title='Book 1', available=True, publisher="Publisher", category=self.category)
        self.book2 = Book.objects.create(title='Book 2', available=False, publisher="Publisher", category=self.category)

        # Set up client and login the user
        self.client = APIClient()
        self.client.login(email='testuser@example.com', password='testpass')

    def test_available_books(self):
        url = reverse('available_books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 book should be available

    def test_get_a_book(self):
        url = reverse('get_a_book', args=[self.book1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Book 1')

    
    def test_filter_books_by_category(self):
        url = reverse('filter_books_by_category')
        response = self.client.get(url, {'category_name': self.category.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books with the same category

    
    def test_filter_books_by_publisher(self):
        url = reverse('filter_books_by_publishers')
        response = self.client.get(url, {'publisher_name': "Publisher"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two books with the same publisher
