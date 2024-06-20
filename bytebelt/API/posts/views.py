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

class PostListCreate(generics.ListCreateAPIView):
    queryset = Posts.objects.all()  # Définir queryset au niveau de la classe
    serializer_class = PostSerializer  # Définir le serializer_class

    def post(self, request):
        queryset = Posts.objects.all()  # Define the queryset at the class level
        serializer_class = PostSerializer  # Define the serializer class

        def perform_create(self, serializer):
            serializer.save(user=self.request.user)  # Automatically associate the post with the logged-in user

        def post(self, request, *args, **kwargs):
            return super().post(request, *args, **kwargs)  
    
    