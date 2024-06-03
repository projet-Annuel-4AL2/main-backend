from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import render
from .models import CustomUser
from rest_framework import generics
from .serializers import UserSerializer
from .filters import UserFilter
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status



class UserListCreate(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    
class AddFollower(APIView):
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        follower = get_object_or_404(CustomUser, pk=request.data['follower_id'])
        user.followers.add(follower)
        return Response({'status': 'follower added'}, status=status.HTTP_200_OK)