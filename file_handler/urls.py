from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_files, name='upload_files'),
    path('random-line/<str:filename>/', views.random_line, name='random_line'),
    path('random-line-backwards/<str:filename>/', views.random_line_backwards, name='random_line_backwards'),
    path('longest-100-lines/', views.longest_100_lines, name='longest_100_lines'),
    path('longest-20-lines/<str:filename>/', views.longest_20_lines, name='longest_20_lines'),
]
