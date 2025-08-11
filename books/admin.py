from django.contrib import admin
from .models import Book, BookPage, Favorite

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year', 'genre', 'page_count', 'created_at']
    list_filter = ['genre', 'year', 'created_at']
    search_fields = ['title', 'author', 'description']
    readonly_fields = ['page_count', 'cover_image', 'created_at', 'updated_at']

@admin.register(BookPage)
class BookPageAdmin(admin.ModelAdmin):
    list_display = ['book', 'page_number']
    list_filter = ['book']

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'created_at']
    list_filter = ['created_at']
