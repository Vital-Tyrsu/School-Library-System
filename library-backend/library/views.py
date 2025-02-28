from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Student, Book, BorrowingRecord
from .serializers import StudentSerializer, BookSerializer, BorrowingRecordSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def borrow_book(self, request, pk=None):
        book = get_object_or_404(Book, pk=pk)
        if book.status != 'Available':
            return Response({'error': 'Book is not available'}, status=status.HTTP_400_BAD_REQUEST)

        student_id = request.data.get('student_id')
        student = get_object_or_404(Student, pk=student_id)

        due_date = request.data.get('due_date')
        if not due_date or due_date <= timezone.now().date():
            return Response({'error': 'Due date must be in the future'}, status=status.HTTP_400_BAD_REQUEST)

        borrowing_record = BorrowingRecord.objects.create(
            student=student,
            book=book,
            due_date=due_date
        )
        book.status = 'Borrowed'
        book.save()

        serializer = BorrowingRecordSerializer(borrowing_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BorrowingRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowingRecord.objects.all()
    serializer_class = BorrowingRecordSerializer

    def return_book(self, request, pk=None):
        borrowing_record = get_object_or_404(BorrowingRecord, pk=pk)
        if borrowing_record.return_date:
            return Response({'error': 'Book has already been returned'}, status=status.HTTP_400_BAD_REQUEST)

        borrowing_record.return_date = timezone.now().date()
        borrowing_record.book.status = 'Available'
        borrowing_record.book.save()

        # Calculate overdue fee if return_date > due_date
        if borrowing_record.return_date > borrowing_record.due_date:
            days_overdue = (borrowing_record.return_date - borrowing_record.due_date).days
            borrowing_record.overdue_fee = max(0, days_overdue * 0.50)  # $0.50 per day overdue
            borrowing_record.save()

        serializer = BorrowingRecordSerializer(borrowing_record)
        return Response(serializer.data, status=status.HTTP_200_OK)