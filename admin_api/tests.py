from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from user.models import User
from book.models import Book, BorrowBook, Category
from datetime import timedelta, date
from rest_framework.test import force_authenticate
from django.utils import timezone

class LibraryTest(APITestCase):
    
    def setUp(self):
        # Create a test admin user
        self.admin_user = User.objects.create_superuser(email='testadmin@example.com', password='admin123')
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
        # Create a category
        self.category = Category.objects.create(name='Fiction')

        # Create a test book
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publisher="Test Publisher",
            category=self.category,
            available=True
        )
        
        # Create a test user
        self.user = User.objects.create_user(email='testuser@example.com', password='user123')
        
    def test_add_book(self):
        # Test adding a book
        data = {
            "title": "New Book",
            "author": "New Author",
            "publisher": "New Publisher",
            "category": self.category.id,
            "available": True
        }
        response = self.client.post('/admin_api/add_book/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], "New Book")

    def test_remove_book(self):
        # Test removing a book
        response = self.client.delete(f'/admin_api/remove_book/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Test removing a non-existing book
        response = self.client.delete(f'/admin_api/remove_book/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_users(self):
        # Test listing users
        response = self.client.get('/admin_api/list_users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Includes admin and user1

    def test_list_users_with_borrowed_books(self):
        # Borrow a book
        borrowed_book = BorrowBook.objects.create(
            user=self.user, 
            book=self.book, 
            duration_in_days=7, 
            return_date=timezone.now() + timedelta(days=7)
        )
        borrowed_book.save()

        # Test listing users with borrowed books
        response = self.client.get('/admin_api/list_users_with_borrowed_books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check if 'borrowed_books' is in the response
        self.assertTrue('borrowed_books' in response.data[0])  # Adjusted: check 'borrowed_books' in top level of response
        self.assertTrue('id' in response.data[0])  # Check that 'user' data is included (like 'id', 'name', etc.)


    def test_list_unavailable_books(self):
        # Mark book as unavailable
        self.book.available = False
        self.book.save()

        # Test listing unavailable books
        response = self.client.get('/admin_api/list_unavailable_books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one book is unavailable

