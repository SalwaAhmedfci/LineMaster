from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Define a simple homepage view
def homepage(request):
    return HttpResponse("<h1>Welcome to Line Master API</h1>")

# URL configuration
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin site
    path('', homepage, name='homepage'),  # Homepage route
    path('api/', include('file_handler.urls')),  # Include file handler app's URLs
]
