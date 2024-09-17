from django.db import models
from user.models import User
from datetime import timedelta


# Model for Categories
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Model for Publishers


# Model for Books
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publisher = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="books")
    available = models.BooleanField(default=True)  # Indicates if the book is available for borrowing
    borrowed_until = models.DateField(null=True, blank=True)  # When the book is expected to be returned
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} by {self.author}"

    # Helper to check availability
    def is_available(self):
        return self.available

# Model for Borrowing
class BorrowBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    duration_in_days = models.PositiveIntegerField()  # How long the books are borrowed for in days
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField()  # Calculated based on duration

    def save(self, *args, **kwargs):
    # Set the return date based on the borrow date and duration
        if not self.return_date:
            self.return_date = self.borrow_date + timedelta(days=self.duration_in_days)
        super().save(*args, **kwargs)

        # Update the book's availability status
        self.book.available = False
        self.book.borrowed_until = self.return_date
        self.book.save()

    def __str__(self):
        return f"{self.user} borrowed {self.book.count()} books"
