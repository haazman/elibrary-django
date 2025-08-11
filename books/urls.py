from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('catalog/', views.catalog_view, name='catalog'),
    path('book/<int:book_id>/', views.book_detail_view, name='detail'),
    path('upload/', views.upload_book_view, name='upload'),
    path('book/<int:book_id>/edit/', views.edit_book_view, name='edit'),
    path('book/<int:book_id>/delete/', views.delete_book_view, name='delete'),
    path('book/<int:book_id>/read/', views.read_book_view, name='read'),
    path('book/<int:book_id>/toggle-favorite/', views.toggle_favorite_view, name='toggle_favorite'),
    path('book/<int:book_id>/analyze/', views.analyze_book_view, name='analyze'),
]
