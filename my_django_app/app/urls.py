from django.urls import path
from .views import handle_post

urlpatterns = [
    path('download/', handle_post, name='file_download'),
]