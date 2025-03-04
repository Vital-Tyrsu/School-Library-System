from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms import ModelForm, DateInput
from import_export.admin import ImportExportModelAdmin
from .models import Book, Student, BorrowingRecord
from .resources import BookResource
from import_export.formats import base_formats
from datetime import date

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = ('title', 'author', 'genre', 'isbn', 'status', 'publication_year')
    formats = (base_formats.JSON, base_formats.CSV)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'registration_date')

class BorrowingRecordAdminForm(ModelForm):
    class Meta:
        model = BorrowingRecord
        fields = '__all__'
        widgets = {
            'borrow_date': DateInput(attrs={'type': 'date'}),
            'due_date': DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        borrow_date = cleaned_data.get('borrow_date')
        due_date = cleaned_data.get('due_date')

        if borrow_date and due_date and due_date <= borrow_date:
            raise ValidationError("Due date must be later than the borrow date.")

        if book:
            existing_borrow = BorrowingRecord.objects.filter(
                book=book,
                return_date__isnull=True
            ).first()

            if existing_borrow:
                raise ValidationError(f"This book is already borrowed by {existing_borrow.student.name} until {existing_borrow.due_date}.")

        return cleaned_data

@admin.register(BorrowingRecord)
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrow_date', 'due_date', 'return_date', 'overdue_fee')
    form = BorrowingRecordAdminForm

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
            messages.success(request, f"Borrowing record for {obj.book.title} has been created successfully for {obj.student.name}.")
        except ValidationError as e:
            messages.error(request, str(e))
            return
