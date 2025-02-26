from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),  # Includes the library app's URLs under /api/
    path('', include('library.urls')),  # Add this to handle the root URL
]