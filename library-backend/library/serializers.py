from rest_framework import serializers
from .models import Student, Book, BorrowingRecord

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'email', 'registration_date']  # Exclude password for security

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'isbn', 'status', 'publication_year']

class BorrowingRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BorrowingRecord
        fields = ['id', 'student', 'book', 'borrow_date', 'due_date', 'return_date', 'overdue_fee']