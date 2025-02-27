from import_export import resources
from .models import Book

class BookResource(resources.ModelResource):
    class Meta:
        model = Book
        fields = ('title', 'author', 'genre', 'isbn', 'status', 'publication_year')