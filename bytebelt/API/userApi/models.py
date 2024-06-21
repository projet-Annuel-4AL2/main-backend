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