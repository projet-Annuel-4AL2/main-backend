# API/userApi/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'username', 'password', 'is_active' , 'created_at', 'updated_at' , 'role']
