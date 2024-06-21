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
    #envoyer tous users
    token = request.session.get('token')
    response = requests.get(API_BASE_URL + 'users/')
    user = requests.post(API_BASE_URL + 'user/', data={'token': token})
    if response.status_code == 200 and user.status_code == 200:
        users = response.json()
        user = user.json()
        return render(request, 'home.html', {'users': users , 'user': user})
    else:
        return render(request, 'home.html', {'error': 'Unable to fetch users'})
    

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
                    return render(request, 'home.html')
                    
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
                return render(request, 'home.html')
            else:
                error = response.json().get('error', 'Error registering user via API')
                return render(request, 'register.html', {'error': error})
        except requests.RequestException:
            return render(request, 'register.html', {'error': 'Error connecting to API'})
    
    return render(request, 'register.html')

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