from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'username', 'password', 'is_active' , 'created_at', 'updated_at' , 'role']
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    