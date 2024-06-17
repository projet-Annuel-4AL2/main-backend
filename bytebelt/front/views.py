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
from rest_framework.authtoken.models import Token


API_BASE_URL = config('API_BASE_URL')

def home(request):
    token = request.session.get('token')
    if token:
        return render(request, 'home.html', {'token': token})

    else:
        return redirect('login')

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
                    return render(request, 'home.html' , {'token': token})
                    
                else:
                    return render(request, 'login.html', {'error': 'Invalid credentials'})
            else:
                return render(request, 'login.html', {'error': 'error api'})
                        
    return render(request, 'login.html')

def register(request):
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
    token_key = request.session.get('token')
    if token_key:
        try:
            token = Token.objects.get(key=token_key)
            user = token.user
            token.delete()
            del request.session['token']

            logout(request)
        except Token.DoesNotExist:
            pass

    return redirect('login')

@csrf_exempt
def execute_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            language = data.get('language')
            code = data.get('code')

            if language == 'php':
                # Exécutez le code PHP avec subprocess
                try:
                    output = subprocess.check_output(['php', '-r', code], universal_newlines=True)
                except subprocess.CalledProcessError as e:
                    output = e.output
            elif language == 'python':
                try:
                    output = subprocess.check_output(['python', '-c', code], universal_newlines=True)
                except subprocess.CalledProcessError as e:
                    output = e.output
            elif language == 'javascript':
                try:
                    output = subprocess.check_output(['node', '-e', code], universal_newlines=True)
                except subprocess.CalledProcessError as e:
                    output = e.output
            else:
                output = "Langage non pris en charge"

            return JsonResponse({'output': output})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON invalide'}, status=400)

    return JsonResponse({'error': 'Méthode de requête non autorisée'}, status=405)
