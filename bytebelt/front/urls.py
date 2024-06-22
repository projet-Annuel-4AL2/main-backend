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
    path('follow/<uuid:pk>/', views.userDetail, name='follow'),
    path('feed/', views.feed, name='feed'),
    path('explorer/', views.explorer, name='explorer'),
]