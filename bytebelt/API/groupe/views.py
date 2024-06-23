from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Groupe , GroupePublication , CommentPublication
from .serializers import GroupeSerializer , GroupePublicationSerializer
from django.http import Http404
from rest_framework.permissions import AllowAny
from API.userApi.models import CustomUser
from django.shortcuts import get_object_or_404


class CreateGroupeView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, format=None):
        serializer = GroupeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CreatePostForGroupeViewByGroupeId(APIView):
    permission_classes = [AllowAny]
    def post(self, request ,*args, **kwargs):
        groupe_id = request.data['groupe']
        try:
            groupe = Groupe.objects.get(id=groupe_id)
        except Groupe.DoesNotExist:
            raise Http404
        serializer = GroupePublicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetAllGroupeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        groupes = Groupe.objects.all()
        serializer = GroupeSerializer(groupes, many=True)
        return Response(serializer.data)

class GetGroupeByName(APIView):
    permission_classes = [AllowAny]
    def get(self, request, name, format=None):
        try:
            groupe = Groupe.objects.get(name=name)
        except Groupe.DoesNotExist:
            raise Http404
        serializer = GroupeSerializer(groupe)
        return Response(serializer.data)
    
class GetAllPostForGroupeView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, groupe_id, format=None):
        try:
            groupe = Groupe.objects.get(id=groupe_id)
        except Groupe.DoesNotExist:
            raise Http404
        publications = groupe.groupepublication_set.all().order_by('-created_at')
        serializer = GroupePublicationSerializer(publications, many=True)
        return Response(serializer.data)

class LikePublicationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, publication_id):
        publication = get_object_or_404(GroupePublication, id=publication_id)
        user_id = request.data.get('author')
        user = get_object_or_404(CustomUser, id=user_id)

        if user in publication.likes.all():
            publication.likes.remove(user)
            message = 'Unliked'
        else:
            publication.likes.add(user)
            message = 'Liked'

        publication.save()
        return Response({'status': message}, status=status.HTTP_200_OK)
    
class CommentPublicationView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, publication_id):
        publication = get_object_or_404(GroupePublication, id=publication_id)
        user_id = request.data.get('author')
        user = get_object_or_404(CustomUser, id=user_id)
        
        comment = CommentPublication.objects.create(
            publication=publication,
            author=user,
            content=request.data.get('content')
        )
        
        return Response({'status': 'comment added'}, status=status.HTTP_200_OK)
    
class GetPublicationGroupeById(APIView):
    permission_classes = [AllowAny]
    def get(self, request, publication_id , groupe_name , format=None):
        try:
            groupe = Groupe.objects.get(name=groupe_name)
        except Groupe.DoesNotExist:
            raise Http404
        try:
            publication = groupe.groupepublication_set.get(id=publication_id)
        except GroupePublication.DoesNotExist:
            raise Http404
        serializer = GroupePublicationSerializer(publication)
        return Response(serializer.data)
    
    
        