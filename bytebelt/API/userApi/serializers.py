from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'username', 'password', 'is_active' ,'created_at', 'updated_at' , 'role']
        read_only_fields = ['is_active']
    
    def validate_password(self , value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value
        
        
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    