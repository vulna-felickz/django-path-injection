from django.urls import path
from app.views import handle_post

urlpatterns = [
    path('download/', handle_post, name='file_download'),
]