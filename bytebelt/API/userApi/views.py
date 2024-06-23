from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import render
from .models import CustomUser
from rest_framework import generics
from .serializers import UserSerializer
from .AuthTokenSerializer import AuthTokenSerializer
from .filters import UserFilter
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed







class UserListCreate(generics.ListCreateAPIView):
    permission_classes = [AllowAny] 
    queryset = CustomUser.objects.all().order_by('-created_at')
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    
class UserInfo(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        token_header = request.data.get('token')
        if token_header is not None:
            try:
                token = Token.objects.get(key=token_header)
                user = token.user
                user_info = get_object_or_404(CustomUser, id=user.id)
                return Response(UserSerializer(user_info).data, status=status.HTTP_200_OK)
            except Token.DoesNotExist:
                raise AuthenticationFailed('Invalid token')
        else:
            raise AuthenticationFailed('Authentication token were not provided.')
        
class UpdateUser(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        token_header = request.headers.get('Authorization')
        if token_header is not None:
            try:
                token_key = token_header.split(' ')[1]
                token = Token.objects.get(key=token_key)
                user = token.user
                user_info = get_object_or_404(CustomUser, id=user.id)
                user_info.username = request.data.get('username')
                user_info.email = request.data.get('email')
                user_info.profile_pic = request.data.get('profile_pic')
                user_info.save()
                return Response({'status': 'user updated'}, status=status.HTTP_200_OK)
            except (Token.DoesNotExist, IndexError):
                raise AuthenticationFailed('Invalid token')
        else:
            raise AuthenticationFailed('Authentication credentials were not provided.')
             
class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny] 
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    

class GetUserByName(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter = {}
        username = self.kwargs.get('username', None)
        if username is not None:
            filter['username'] = username
        return get_object_or_404(queryset, **filter)
    
class AddFollower(APIView):
    permission_classes = [AllowAny]
    def post(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        follower = get_object_or_404(CustomUser, pk=request.data['follower_id'])
        user.followers.add(follower)
        return Response({'status': 'follower added'}, status=status.HTTP_200_OK)

class GetAllFollowers(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        followers = user.followers.all()
        return Response({'followers': UserSerializer(followers, many=True).data}, status=status.HTTP_200_OK)

class GetAllFollowing(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        following = user.following.all()
        return Response({'followings': UserSerializer(following, many=True).data}, status=status.HTTP_200_OK)
    
class UserAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'id': user.id
        })
    
class RegisterUser(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            if CustomUser.objects.filter(username=username).exists():
                return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
            if CustomUser.objects.filter(email=email).exists():
                return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PasswordReset(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            return Response({'status': 'email valid'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'email invalid'}, status=status.HTTP_404_NOT_FOUND)
        
class ChangePassword(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        email= request.data.get('email')
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            user.set_password(password)
            user.save()
            return Response({'status': 'password changed'}, status=status.HTTP_200_OK)
        return Response({'error': 'user not found'}, status=status.HTTP_404_NOT_FOUND)
        
