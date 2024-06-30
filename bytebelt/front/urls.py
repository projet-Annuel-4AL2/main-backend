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
    path('updatePassword/', views.updatePassword, name='updatePassword'),
    #path('follow/<uuid:pk>/', views.userDetail, name='follow'),
    path('profil/<str:username>/', views.userInfos, name='profil'),
    path('feed/', views.feed, name='feed'),
    path('explorer/', views.explorer, name='explorer'),
    path('group/<name>/', views.groupInfo, name='group'),
    path('group/<name>/post/', views.groupPost, name='groupPost'),
    path('group/<name>/post/<id>', views.groupPostInfo, name='groupPostInfo'),
    path('deleteGroupPost/<id>/', views.deleteGroupPost, name='deleteGroupPost'),
    #path('addComment/<groupe_name>/<id>/', views.addComment, name='addComment'),
    path('users_/', views.get_all_users_view, name='users_'),
    path('followers/', views.followers, name='followers'),
    path('groupe/create/', views.createGroupe, name='createGroupe'),
    path('<name>/settings/', views.userSettings, name='userSettings'),
    path('delete/<name>/', views.deleteUser, name='deleteUser'),
    
    
    
    
    
    ######code session
    path('codeSession/<int:post_id>', views.codeSession, name='codeSession'),
    path('runCode/', views.runCode, name='runCode'),
]