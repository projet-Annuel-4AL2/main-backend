from django.urls import path
from .views import PostListCreate

urlpatterns = [
    path('posts/', PostListCreate.as_view(), name='post-list-create'),


]
