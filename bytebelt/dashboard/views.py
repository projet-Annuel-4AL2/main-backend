from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json




# Create your views here.

def dashboard(request):
    return render(request, "dashboard.html")