from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, BookViewSet, BorrowingRecordViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrowing', BorrowingRecordViewSet, basename='borrowing')

urlpatterns = [
    path('', include(router.urls)),
    path('books/<int:pk>/borrow/', BookViewSet.as_view({'post': 'borrow_book'}), name='borrow_book'),
    path('borrowing/<int:pk>/return/', BookViewSet.as_view({'post': 'return_book'}), name='return_book'),
]