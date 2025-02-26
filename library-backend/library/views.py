from rest_framework import viewsets, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Student, Book, BorrowingRecord
from .serializers import StudentSerializer, BookSerializer, BorrowingRecordSerializer
from django.utils import timezone

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

        # For now, assume student ID is provided (we’ll handle authentication later)
        student_id = request.data.get('student_id')
        student = get_object_or_404(Student, pk=student_id)

        # Create borrowing record and update book status
        borrowing_record = BorrowingRecord.objects.create(
            student=student,
            book=book,
            due_date=request.data.get('due_date', None) or (timezone.now() + timezone.timedelta(days=14))  # 2-week loan by default
        )
        book.status = 'Borrowed'
        book.save()

        serializer = BorrowingRecordSerializer(borrowing_record)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def return_book(self, request, pk=None):
        borrowing_record = get_object_or_404(BorrowingRecord, pk=pk)
        if borrowing_record.return_date:
            return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate overdue fee (simplified: $0.50 per day overdue)
        from django.utils import timezone
        days_overdue = (timezone.now().date() - borrowing_record.due_date).days
        overdue_fee = max(0, days_overdue * 0.50)
        borrowing_record.return_date = timezone.now().date()
        borrowing_record.overdue_fee = overdue_fee
        borrowing_record.save()

        book = borrowing_record.book
        book.status = 'Available'
        book.save()

        serializer = BorrowingRecordSerializer(borrowing_record)
        return Response(serializer.data, status=status.HTTP_200_OK)

class BorrowingRecordViewSet(viewsets.ModelViewSet):
    queryset = BorrowingRecord.objects.all()
    serializer_class = BorrowingRecordSerializer