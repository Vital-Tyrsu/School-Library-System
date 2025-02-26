from rest_framework import viewsets
from .models import Student, Book, BorrowingRecord
from .serializers import StudentSerializer, BookSerializer, BorrowingRecordSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BorrowingRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowingRecord.objects.all()
    serializer_class = BorrowingRecordSerializer
