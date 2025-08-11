from django import forms
from .models import Book

class BookUploadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file', 'title', 'description', 'author', 'year', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-input', 'accept': '.pdf'}),
        }
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file:
            if not pdf_file.name.endswith('.pdf'):
                raise forms.ValidationError('Hanya file PDF yang diperbolehkan.')
        return pdf_file

class BookEditForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['pdf_file', 'title', 'description', 'author', 'year', 'genre']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'year': forms.NumberInput(attrs={'class': 'form-input'}),
            'genre': forms.Select(attrs={'class': 'form-select'}),
            'pdf_file': forms.FileInput(attrs={'class': 'form-input', 'accept': '.pdf'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pdf_file'].required = False
    
    def clean_pdf_file(self):
        pdf_file = self.cleaned_data.get('pdf_file')
        if pdf_file and not pdf_file.name.endswith('.pdf'):
            raise forms.ValidationError('Hanya file PDF yang diperbolehkan.')
        return pdf_file

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Cari berdasarkan judul, tahun, atau deskripsi...'
        }),
        label=''
    )
