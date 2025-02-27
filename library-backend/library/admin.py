from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Book
from .resources import BookResource
from import_export.formats import base_formats

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    pass
    