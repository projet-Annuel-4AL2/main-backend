from rest_framework import serializers
from django.contrib.auth.models import User 
from .models import CustomUser , UserPost
import re

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'username', 'password', 'is_active' ,'created_at', 'updated_at' , 'role' ,'profile_pic', 'followers' , 'bio']
        read_only_fields = [ 'is_active','followers']
    
    def validate_password(self , value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
    
    def validate_username(self , value):
        value =re.sub(r"[ -_!@#$%^&*(){}[\]:;\"'<>?,./]", "", value)
        return value
        
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

class UserPostSerializer(serializers.ModelSerializer):
    #author = UserSerializer(read_only=True)
    likes = UserSerializer(read_only=True, many=True)
    comments = UserSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = UserPost
        fields = '__all__'