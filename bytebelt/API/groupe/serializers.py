from rest_framework import serializers
from .models import Groupe, GroupePublication , CommentPublication
from API.userApi.serializers import UserSerializer  
import re

class GroupeSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    admin = UserSerializer(read_only=True)
    class Meta:
        model = Groupe
        fields = '__all__'
        
    def validate_name(self, value):
        value = re.sub(r"[ -_!@#$%^&*(){}[\]:;\"'<>?,./]", "", value)
        return value
        


class GroupePublicationSerializer(serializers.ModelSerializer):
    likes = UserSerializer(read_only=True, many=True)
    comments = UserSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = GroupePublication
        fields = '__all__'


class CommentPublicationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = CommentPublication
        fields = '__all__'