from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from import_export.admin import ImportExportModelAdmin
from .models import Book, Student, BorrowingRecord
from .resources import BookResource
from import_export.formats import base_formats

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

    def clean(self):
        cleaned_data = super().clean()
        book = cleaned_data.get('book')
        if book and book.status == 'Borrowed':
            raise ValidationError("This book is already borrowed and cannot be borrowed again.")
        borrow_date = cleaned_data.get('borrow_date')
        due_date = cleaned_data.get('due_date')
        if borrow_date and due_date and due_date <= borrow_date:
            raise ValidationError("Due date must be later than the borrow date.")

@admin.register(BorrowingRecord)
class BorrowingRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'book', 'borrow_date', 'due_date', 'return_date', 'overdue_fee')
    form = BorrowingRecordAdminForm

    def save_model(self, request, obj, form, change):
        try:
            if obj.borrow_date and obj.due_date and obj.due_date <= obj.borrow_date:
                messages.error(request, "Due date must be later than the borrow date.")
                return
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            messages.error(request, str(e))
            return

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj:  # When editing an existing record
            borrow_date = obj.borrow_date
            due_date = form.instance.due_date
            if borrow_date and due_date and due_date <= borrow_date:
                messages.error(request, "Due date must be later than the borrow date.")
                return None  # Prevent form submission if invalid
        return form