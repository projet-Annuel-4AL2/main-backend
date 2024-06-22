from rest_framework import serializers
from .models import Groupe, GroupePublication
from API.userApi.serializers import UserSerializer  

class GroupeSerializer(serializers.ModelSerializer):
    members = UserSerializer(read_only=True, many=True)
    admin = UserSerializer(read_only=True)

    class Meta:
        model = Groupe
        fields = '__all__'

class GroupePublicationSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = UserSerializer(read_only=True, many=True)
    comments = UserSerializer(read_only=True, many=True)

    class Meta:
        model = GroupePublication
        fields = '__all__'