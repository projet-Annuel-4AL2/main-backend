from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import subprocess
import json
import os

API_BASE_URL = os.getenv('API_BASE_URL')


@login_required
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'GET':
        email = request.POST['email']
        password = request.POST['password']
        response = request.post(API_BASE_URL + 'users/', data={'email': email, 'password': password})
        if response.status_code == 200:
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def logout(request):
    logout(request)
    return redirect('login')