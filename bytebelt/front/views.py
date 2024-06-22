import subprocess
import json
import requests
import hashlib
from decouple import config
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , get_user_model , login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

API_BASE_URL = config('API_BASE_URL')


def token_required(view_func):
    def wrapper(request, *args, **kwargs):
        token = request.session.get('token')
        if not token:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper  

@token_required
def home(request):
    if not request.session.get('token'):
        return redirect('login')
    
    user_data = get_user_data(request)
    if user_data:
        return render(request, 'home.html', {
            'users': user_data.get('users'),
            'user': user_data.get('user'),
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings'),
            'groupes': user_data.get('groupes')
        })
    else:
        return render(request, 'home.html', {'error': 'Unable to fetch user data'})
    
def feed(request):
    if not request.session.get('token'):
        return redirect('login')
    
    user_data = get_user_data(request)
    if(user_data):
        return render(request, 'feed.html', {
            'users': user_data.get('users'),
            'user': user_data.get('user'),
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings')
        })
    else:
        return render(request, 'feed.html', {'error': 'Unable to fetch user data'})
    
def explorer(request):
    if not request.session.get('token'):
        return redirect('login')
    
    user_data = get_user_data(request)
    if user_data:
        return render(request, 'explorer.html', {
            'users': user_data.get('users'),
            'user': user_data.get('user'),
            'followers': user_data.get('followers'),
            'followings': user_data.get('followings')
        })
    else:
        return render(request, 'explorer.html', {'error': 'Unable to fetch user data'})

@token_required
def userDetail (request , pk):
    response = requests.get(API_BASE_URL + 'users/' + str(pk) + '/')
    user_info = requests.post(API_BASE_URL + 'user/', data={'token': request.session.get('token')})
    if response.status_code == 200 and user_info.status_code == 200:
        user = response.json()
        user_info = user_info.json()        
        return render(request, 'userDetail.html', {'user': user , 'user_info': user_info})
    else:
        redirect('home')
        
def get_user_data(request):
    token = request.session.get('token')
    user_response = requests.post(API_BASE_URL + 'user/', data={'token': token})
    response = requests.get(API_BASE_URL + 'users/')
    if user_response.status_code == 200 and response.status_code == 200:
        users = response.json()
        user = user_response.json()
        followers_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followers/')
        followings_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followings/')
        groupes = requests.get(API_BASE_URL + 'groupe/')
        if followers_response.status_code == 200 and followings_response.status_code == 200:
            return {
                'users': users,
                'user': user,
                'followers': followers_response.json(),
                'followings': followings_response.json(),
                'groupes': groupes.json()
            }
    return None

        
def login(request):
    if request.session.get('token'):
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')        
        password = request.POST.get('password')

        if not username or not password:
            return render(request, 'login.html', {'error': 'username and password are required'}) 

        if username and password:
            
            response = requests.post(API_BASE_URL + 'auth/', data={'username': username, 'password': password})
            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    request.session['token'] = token
                    user_data = get_user_data(request)
                    return render(request, 'home.html' ,{
                                  'users': user_data.get('users') ,
                                  'user': user_data.get('user') , 
                                  'followers': user_data.get('followers') ,
                                  'followings': user_data.get('followings'),
                                  'groupes': user_data.get('groupes')},
                                  )
                    
                else:
                    return render(request, 'login.html', {'error': 'Invalid credentials'})
            else:
                return render(request, 'login.html', {'error': 'error api'})
                        
    return render(request, 'login.html')

def subscribe(request):
    if request.session.get('token'):
            return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if not username or not email or not password or not password2:
            return render(request, 'register.html', {'error': 'All fields are required'})
        if password != password2:
            return render(request, 'register.html', {'error': 'Passwords do not match'})
        
        try:
            response = requests.post(API_BASE_URL + 'register/', data={'username': username, 'email': email, 'password': password})
            if response.status_code == 201:
                request.session['token'] = response.json().get('token')
                user_data = get_user_data(request)
                return render(request, 'home.html' ,{
                                    'users': user_data.get('users') ,
                                    'user': user_data.get('user') , 
                                    'followers': user_data.get('followers') ,
                                    'followings': user_data.get('followings'),
                                    'groupes': user_data.get('groupes')
  
                })
            else:
                error = response.json().get('error', 'Error registering user via API')
                return render(request, 'register.html', {'error': error})
        except requests.RequestException:
            return render(request, 'register.html', {'error': 'Error connecting to API'})
    
    return render(request, 'register.html')

def get_user_data(request):
    token = request.session.get('token')
    user_response = requests.post(API_BASE_URL + 'user/', data={'token': token})
    if user_response.status_code == 200:
        user = user_response.json()
        users = requests.get(API_BASE_URL + 'users/')
        followers_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followers/')
        followings_response = requests.get(API_BASE_URL + 'users/' + str(user['id']) + '/followings/')
        groupes = requests.get(API_BASE_URL + 'groupe/')
        if followers_response.status_code == 200 and followings_response.status_code == 200 and users.status_code == 200 and groupes.status_code == 200:
            return {
                'users': users.json(),
                'user': user,
                'followers': followers_response.json(),
                'followings': followings_response.json(),
                'groupes': groupes.json()
            }
    return None


def resetPassword(request):
    return render(request, 'resetPassword.html')


def logout(request):
    del request.session['token']
    return redirect('login')

@token_required
def profile(request):
    #get user info by token in session
    token = request.session.get('token')
    response = requests.post(API_BASE_URL + 'user/', data={'token': token})
    if response.status_code == 200:
        user = response.json()
        return render(request, 'profile.html', {'user': user})
    else:
        return render(request, 'profile.html', {'error': 'Unable to fetch user info'})
    
    

def updateP(request):
    username = request.user.username
    email = request.user.email
    profile_pic = request.user.profile_pic

    data = {'username': username, 'email': email, 'profile_pic': profile_pic}

    return render(request, 'updateProfile.html', data)
    
    
    
    
def updateProfile(request):
    if request.method == 'POST':
        token = request.session.get('token')
        username = data.get('username')
        email = data.get('email')
        profile_pic = data.get('profile_pic')
        data = {'username': username, 'email': email}
        if profile_pic:
            data['profile_pic'] = profile_pic
        response = requests.post(API_BASE_URL + 'updateuser/', headers={'Authorization': 'Token ' + token}, data=data)
        if response.status_code == 200:
            return render(request, 'profile.html', {'success': 'Profile updated successfully'})
        else:
            return render(request, 'profile.html', {'error': 'Error updating profile'})
    return render(request, 'profile.html', {'error': 'Invalid request'})


def groupInfo(request , name):
    response = requests.get(API_BASE_URL + 'groupe/info/' + name + '/')
    groupe_id = response.json().get('id')
    posts = requests.get(API_BASE_URL + 'groupe/publications/' + str(groupe_id) + '/')
    if response.status_code == 200 and posts.status_code == 200:
        groupe = response.json()
        posts = posts.json()
        return render(request, 'groupInfo.html', {'groupe': groupe , 'posts': posts})
    else:
        return render(request, 'groupInfo.html', {'error': 'Unable to fetch group info'})
    