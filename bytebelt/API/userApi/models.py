import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100 , unique=True)
    email = models.EmailField(max_length=100 , unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    role = models.CharField(max_length=100 , default="user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField('self', related_name='following', symmetrical=False)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True , null=True)
    

class UserPost(models.Model):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    code = models.TextField(blank=True, null=True)
    language = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='post_likes', blank=True)
    comments = models.ManyToManyField(CustomUser, related_name='post_comments', blank=True)
    image = models.ImageField(upload_to='post_pics/', null=True, blank=True)
    
class Comment(models.Model):
    post = models.ForeignKey(UserPost, on_delete=models.CASCADE, related_name='post_comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Device(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token_device = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
