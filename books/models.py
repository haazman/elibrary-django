from django.db import models
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Book(models.Model):
    GENRE_CHOICES = [
        ('fiksi', 'Fiksi'),
        ('komik', 'Komik'),
        ('motivasi', 'Motivasi'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=100)
    year = models.IntegerField()
    genre = models.CharField(max_length=20, choices=GENRE_CHOICES)
    pdf_file = models.FileField(upload_to='books/pdfs/')
    cover_image = models.ImageField(upload_to='books/covers/', null=True, blank=True)
    page_count = models.IntegerField(default=0)
    keywords = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def get_cover_path(self):
        if self.cover_image:
            return self.cover_image.url
        return None

class BookPage(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='pages')
    page_number = models.IntegerField()
    image = models.ImageField(upload_to='books/pages/')
    
    class Meta:
        ordering = ['page_number']
        unique_together = ['book', 'page_number']
    
    def __str__(self):
        return f"{self.book.title} - Page {self.page_number}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'book']
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
