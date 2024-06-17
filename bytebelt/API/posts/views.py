from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import render
from .models import Posts
from rest_framework import generics
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import PostSerializer

class  PostListCreate(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']
    
