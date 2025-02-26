from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, BookViewSet, BorrowingRecordViewSet

# Create a router and register the viewsets
router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'books', BookViewSet, basename='book')
router.register(r'borrowing', BorrowingRecordViewSet, basename='borrowing')

# Define the URL patterns
urlpatterns = [
    path('', include(router.urls)),
]