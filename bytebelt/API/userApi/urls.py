from django.urls import path
from .views import UserListCreate, UserDetail , AddFollower , UserAuthToken , RegisterUser , PasswordReset , ChangePassword , GetUserByToken

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<uuid:pk>/add-follower/', AddFollower.as_view(), name='add-follower'),
    path('auth/', UserAuthToken.as_view(), name='auth'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('resetpassword/', PasswordReset.as_view(), name='reset-password'),
    path('ChangePassword/', ChangePassword.as_view(), name='change-password'),
    #path('getuserbytoken/', GetUserByToken.as_view(), name='get-user-by-token'),

]
