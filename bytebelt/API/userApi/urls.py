from django.urls import path
from .views import UserListCreate, UserDetail , AddFollower , UserAuthToken

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<uuid:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<uuid:pk>/add-follower/', AddFollower.as_view(), name='add-follower'),
    path('auth/', UserAuthToken.as_view(), name='auth'),

]
