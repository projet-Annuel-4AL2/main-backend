import subprocess
import json
import requests
import hashlib
from decouple import config
from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate , get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

API_BASE_URL = config('API_BASE_URL')

@login_required
def home(request):
    return render(request, 'home.html')

def login(request):
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

def logout(request):
    logout(request)
    return redirect('login')