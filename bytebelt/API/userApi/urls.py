from django.urls import path
from .views import UserListCreate, UserDetail , AddFollower , UserAuthToken , RegisterUser , PasswordReset , ChangePassword , UserInfo , UpdateUser , GetAllFollowers , GetAllFollowing

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<uuid:pk>/add-follower/', AddFollower.as_view(), name='add-follower'),
    path('auth/', UserAuthToken.as_view(), name='auth'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('resetpassword/', PasswordReset.as_view(), name='reset-password'),
    path('ChangePassword/', ChangePassword.as_view(), name='change-password'),
    path('user/', UserInfo.as_view(), name='user-info'),
    path('updateuser/', UpdateUser.as_view(), name='update-user'),
    path('users/<uuid:pk>/followers/', GetAllFollowers.as_view(), name='get-all-followers'),
    path('users/<uuid:pk>/followings/', GetAllFollowing.as_view(), name='get-all-following'),

]
