from django.urls import path
from .views import UserListCreate, UserDetail , AddFollower , UserAuthToken , RegisterUser , PasswordReset , ChangePassword , UserInfo , UpdateUser , GetAllFollowers , GetAllFollowing , GetUserByName, GetFollowingById , UserPostListCreate ,UserPostDetail , AddLike , AddComment , GetComments , GetLikes

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<str:username>/', GetUserByName.as_view(), name='get-user-by-name'),
    path('users/<uuid:pk>/add-follower/', AddFollower.as_view(), name='add-follower'),
    path('users/<uuid:pk>/get-following/', GetFollowingById.as_view(), name='get-follower'),
    path('auth/', UserAuthToken.as_view(), name='auth'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('resetpassword/', PasswordReset.as_view(), name='reset-password'),
    path('ChangePassword/', ChangePassword.as_view(), name='change-password'),
    path('user/', UserInfo.as_view(), name='user-info'),
    path('updateuser/', UpdateUser.as_view(), name='update-user'),
    path('users/<uuid:pk>/followers/', GetAllFollowers.as_view(), name='get-all-followers'),
    path('users/<uuid:pk>/followings/', GetAllFollowing.as_view(), name='get-all-following'),
    ##for user post
    path('post/', UserPostListCreate.as_view(), name='user-post-list-create'),
    path('post/<int:pk>/', UserPostDetail.as_view(), name='user-post-detail'),
    path('post/<int:pk>/add-like/', AddLike.as_view(), name='add-like'),
    path('post/<int:pk>/add-comment/', AddComment.as_view(), name='add-comment'),
    path('post/<int:pk>/get-comment/', GetComments.as_view(), name='get-comments'),
    path('post/<int:pk>/get-like/', GetLikes.as_view(), name='get-likes'),
    

]
