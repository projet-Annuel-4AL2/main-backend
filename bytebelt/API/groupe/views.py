from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Groupe
from .serializers import GroupeSerializer , GroupePublicationSerializer
from django.http import Http404
from rest_framework.permissions import AllowAny

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
    def post(self, request, groupe_id, format=None):
        try:
            groupe = Groupe.objects.get(id=groupe_id)
        except Groupe.DoesNotExist:
            raise Http404
        request.data['groupe'] = groupe_id
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
        publications = groupe.publications.all()
        serializer = GroupePublicationSerializer(publications, many=True)
        return Response(serializer.data)