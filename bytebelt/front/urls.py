from django.urls import path , include
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('logout/', views.logout, name='logout'),
    path('home/', views.home, name='home'),
    path('resetPassword/', views.resetPassword, name='resetPassword'),
    path('profile/', views.profile, name='profile'),
    path('updateProfile/', views.updateProfile, name='updateProfile'),
    path('updateP/', views.updateP, name='updateP'),
    #path('follow/<uuid:pk>/', views.userDetail, name='follow'),
    path('profil/<str:username>/', views.userInfos, name='profil'),
    path('feed/', views.feed, name='feed'),
    path('explorer/', views.explorer, name='explorer'),
    path('group/<name>/', views.groupInfo, name='group'),
    path('group/<name>/post/', views.groupPost, name='groupPost')
]