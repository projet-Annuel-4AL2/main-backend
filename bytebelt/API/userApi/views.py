from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import render
from .models import CustomUser , UserPost , Device
from rest_framework import generics
from .serializers import UserSerializer , UserPostSerializer
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
import secrets






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
                username = request.data.get('username')
                if username is not None:
                    user_info.username = username
                email = request.data.get('email')
                if email is not None:         
                    user_info.email = request.data.get('email')
                bio = request.data.get('bio')
                if bio is not None:
                    user_info.bio = bio
                profile_pic = request.data.get('profile_pic')
                if profile_pic is not None:
                    user_info.profile_pic = profile_pic
                password = request.data.get('password')
                if password is not None:
                    user_info.set_password(password)
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
        
        if follower in user.followers.all():
            user.followers.remove(follower)
            follower.following.remove(user)
            message = 'Unfollowed'  
        else:
            user.followers.add(follower)
            follower.following.add(user)
            message = 'Followed'
            
        return Response({'status': message}, status=status.HTTP_200_OK)

class GetFollowingById(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        following = user.following.all()
        return Response({'following': UserSerializer(following, many=True).data}, status=status.HTTP_200_OK)
    
    
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

class GetUserIdByTokenDevice(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        token_device = request.data.get('token_device')
        if token_device is not None:
            try:
                device = Device.objects.get(token_device=token_device)
                user = device.user
                return Response({'user_id': user.id}, status=status.HTTP_200_OK)
            except Device.DoesNotExist:
                return Response({'error': 'device not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'token device not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
class UserAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if request.data.get('device') is not None:
            token_device , created = Device.objects.get_or_create(user=user)
            token_device.token_device = secrets.token_hex(16)
            token_device.save()
            return Response({
                'token': token_device.token_device,
                'id': user.id,
            })
        else:
            try:
                user.auth_token.delete()
            except:
                pass
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'id': user.id,
                #"token_device": request.data.get('token_device'),
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
            if request.data.get('device') is not None:
                token_device , created = Device.objects.get_or_create(user=user)
                token_device.token_device = secrets.token_hex(16)
                token_device.save()
                token = token_device.token_device,
                return Response({'token': token, 'user': serializer.data}, status=status.HTTP_201_CREATED)  
            else:  
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
        

###for user post

class UserPostListCreate(generics.ListCreateAPIView):
    permission_classes = [AllowAny] 
    queryset = UserPost.objects.all().order_by('-created_at')
    serializer_class = UserPostSerializer
    

class UserPostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny] 
    queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer
  
  
class GetUserPostByUsername(generics.ListCreateAPIView):
    permission_classes = [AllowAny] 
    queryset = UserPost.objects.all()
    serializer_class = UserPostSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        username = self.kwargs.get('username', None)
        if username is not None:
            queryset = queryset.filter(author__username=username)
        return queryset
      
class AddLike(APIView):
    permission_classes = [AllowAny]
    def post(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        user = get_object_or_404(CustomUser, pk=request.data['user_id'])
        
        if user in post.likes.all():
            post.likes.remove(user)
            message = 'Unliked'  
        else:
            post.likes.add(user)
            message = 'Liked'
            
        return Response({'status': message}, status=status.HTTP_200_OK)
    
class AddComment(APIView):
    permission_classes = [AllowAny]
    def post(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        user = get_object_or_404(CustomUser, pk=request.data['user_id'])
        comment = request.data.get('comment')
        if comment is not None:
            post.comments.add(user)
            message = 'Commented'
        return Response({'status': message}, status=status.HTTP_200_OK)
    
class GetComments(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        comments = post.comments.all()
        return Response({'comments': UserSerializer(comments, many=True).data}, status=status.HTTP_200_OK)
    
class GetLikes(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        post = get_object_or_404(UserPost, pk=pk)
        likes = post.likes.all()
        return Response({'likes': UserSerializer(likes, many=True).data}, status=status.HTTP_200_OK)
    