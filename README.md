# E-Library Django Application

A full-featured e-library application built with Django, featuring book management, PDF processing, and text analysis capabilities.

## Features

- **Book Management**: Upload, edit, delete, and organize books
- **Search & Filter**: Advanced search by title, author, year, and genre
- **User Authentication**: Secure login/registration with email
- **PDF Reader**: Built-in PDF viewer with page navigation
- **Favorites**: Mark and filter favorite books
- **Text Analysis**: Keyword extraction using NLTK and scikit-learn
- **Responsive Design**: Mobile-friendly interface with Tailwind CSS

## Technologies Used

- **Backend**: Django 5.2.5
- **Database**: SQLite3
- **Frontend**: Tailwind CSS, Font Awesome 6.0
- **PDF Processing**: PyMuPDF (fitz)
- **Text Analysis**: scikit-learn, NLTK

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation & Setup

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd django_ciheul
```
*Or download and extract the ZIP file*

### 2. Install Required Dependencies
```bash
pip install django PyMuPDF gensim scikit-learn nltk pillow
```

### 3. Set Up the Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Download NLTK Data (Required for Text Analysis)
```bash
python manage.py download_nltk
```

### 5. Create Admin User
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 6. Run the Development Server
```bash
python manage.py runserver
```

### 7. Access the Application
- **Main Application**: http://127.0.0.1:8000
- **Admin Panel**: http://127.0.0.1:8000/admin

## Usage

1. **Register/Login**: Create a new account or login with existing credentials
2. **Upload Books**: Use the upload feature to add PDF books to the library
3. **Browse Catalog**: Explore books with search and filter options
4. **Read Books**: Use the built-in PDF reader to view books
5. **Manage Profile**: Update your profile information and preferences

## Troubleshooting

### Common Issues

**NLTK Data Missing**
```bash
python manage.py download_nltk
```

**Static Files Not Loading**
```bash
python manage.py collectstatic
```

**Database Issues**
```bash
python manage.py makemigrations
python manage.py migrate
```

## Project Structure

```
django_ciheul/
├── elibrary/           # Main Django project settings
├── accounts/           # User authentication and profiles
├── books/              # Book management and PDF processing
├── templates/          # HTML templates
├── static/             # Static files (CSS, JS, images)
├── media/              # Uploaded files (PDFs, covers, profile pics)
├── db.sqlite3          # Database file
└── manage.py           # Django management script
```

## Default Credentials

After creating a superuser, you can access the admin panel with your created credentials.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

For support or questions, please create an issue in the repository or contact the development team.
