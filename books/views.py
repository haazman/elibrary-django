from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import fitz  
import os
from PIL import Image
import io
from .models import Book, BookPage, Favorite
from .forms import BookUploadForm, BookEditForm, SearchForm
from .utils import analyze_book_keywords

@login_required
def catalog_view(request):
    books = Book.objects.all().order_by('-created_at')
    search_form = SearchForm()
    
    search_query = request.GET.get('search')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(year__icontains=search_query)
        )
        search_form = SearchForm(initial={'query': search_query})
    
    favorites_filter = request.GET.get('favorites')
    if favorites_filter == '1':
        favorite_book_ids = Favorite.objects.filter(user=request.user).values_list('book_id', flat=True)
        books = books.filter(id__in=favorite_book_ids)
    
    genre_filter = request.GET.get('genre')
    if genre_filter:
        books = books.filter(genre=genre_filter)
    
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    user_favorites = set()
    if request.user.is_authenticated:
        user_favorites = set(Favorite.objects.filter(user=request.user).values_list('book_id', flat=True))
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'user_favorites': user_favorites,
        'current_filter': {
            'search': search_query,
            'favorites': favorites_filter,
            'genre': genre_filter,
        }
    }
    
    return render(request, 'books/catalog.html', context)

@login_required
def book_detail_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    is_favorite = Favorite.objects.filter(user=request.user, book=book).exists()
    
    context = {
        'book': book,
        'is_favorite': is_favorite,
    }
    
    return render(request, 'books/detail.html', context)

@login_required
def upload_book_view(request):
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            
            try:
                process_pdf_to_images(book)
                messages.success(request, 'Buku berhasil diupload!')
                return redirect('books:detail', book_id=book.id)
            except Exception as e:
                book.delete()
                messages.error(request, f'Gagal memproses PDF: {str(e)}')
    else:
        form = BookUploadForm()
    
    return render(request, 'books/upload.html', {'form': form})

@login_required
def edit_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookEditForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            updated_book = form.save()
            
            if 'pdf_file' in request.FILES:
                BookPage.objects.filter(book=book).delete()
                try:
                    process_pdf_to_images(updated_book)
                except Exception as e:
                    messages.error(request, f'Gagal memproses PDF: {str(e)}')
                    return redirect('books:edit', book_id=book.id)
            
            messages.success(request, 'Buku berhasil diperbarui!')
            return redirect('books:detail', book_id=book.id)
    else:
        form = BookEditForm(instance=book)
    
    return render(request, 'books/edit.html', {'form': form, 'book': book})

@login_required
def delete_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        if book.pdf_file:
            if os.path.exists(book.pdf_file.path):
                os.remove(book.pdf_file.path)
        
        if book.cover_image:
            if os.path.exists(book.cover_image.path):
                os.remove(book.cover_image.path)
        
        for page in book.pages.all():
            if os.path.exists(page.image.path):
                os.remove(page.image.path)
        
        book.delete()
        messages.success(request, 'Buku berhasil dihapus!')
        return redirect('books:catalog')
    
    return render(request, 'books/delete_confirm.html', {'book': book})

@login_required
def read_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    page_number = int(request.GET.get('page', 1))
    
    pages = book.pages.all()
    if not pages:
        messages.error(request, 'Halaman buku tidak ditemukan.')
        return redirect('books:detail', book_id=book.id)
    
    current_page = get_object_or_404(BookPage, book=book, page_number=page_number)
    
    context = {
        'book': book,
        'current_page': current_page,
        'total_pages': pages.count(),
        'page_number': page_number,
    }
    
    return render(request, 'books/read.html', context)

@login_required
@require_POST
def toggle_favorite_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
    
    if not created:
        favorite.delete()
        is_favorite = False
    else:
        is_favorite = True
    
    return JsonResponse({'is_favorite': is_favorite})

@login_required
def analyze_book_view(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    try:
        keywords = analyze_book_keywords(book)
        book.keywords = ', '.join(keywords)
        book.save()
        messages.success(request, 'Analisis kata kunci berhasil!')
    except Exception as e:
        messages.error(request, f'Gagal menganalisis buku: {str(e)}')
    
    return redirect('books:detail', book_id=book.id)

def process_pdf_to_images(book):
    pdf_path = book.pdf_file.path
    doc = fitz.open(pdf_path)
    
    first_page = doc[0]
    pix = first_page.get_pixmap()
    img_data = pix.tobytes("png")
    
    cover_filename = f"cover_{book.id}.png"
    cover_path = os.path.join('media/books/covers/', cover_filename)
    os.makedirs(os.path.dirname(cover_path), exist_ok=True)
    
    with open(cover_path, 'wb') as f:
        f.write(img_data)
    
    book.cover_image = f'books/covers/{cover_filename}'
    book.page_count = len(doc)
    book.save()
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        pix = page.get_pixmap()
        img_data = pix.tobytes("png")
        
        page_filename = f"book_{book.id}_page_{page_num + 1}.png"
        page_path = os.path.join('media/books/pages/', page_filename)
        os.makedirs(os.path.dirname(page_path), exist_ok=True)
        
        with open(page_path, 'wb') as f:
            f.write(img_data)
        
        BookPage.objects.create(
            book=book,
            page_number=page_num + 1,
            image=f'books/pages/{page_filename}'
        )
    
    doc.close()
