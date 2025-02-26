from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),
    path('', include('library.urls')),  # Handle root URL (optional)
]