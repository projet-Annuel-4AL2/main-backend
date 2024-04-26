from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import ctypes



def home(request):
    return render(request, "index.html")

@csrf_exempt
def execute_code(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        code = request.POST.get('code')

        if language == 'php':
            # Exéc PHP avec subprocess
            try:
                output = subprocess.check_output(['php', '-r', code], universal_newlines=True)
            except subprocess.CalledProcessError as e:
                output = e.output
        elif language == 'python':
            try:
                output = str(eval(code))
            except Exception as e:
                output = str(e)   
        else:
            output = "Langage non pris en charge"

        return JsonResponse({'output': output})


    return JsonResponse({'error': 'Méthode de requête non autorisée'}, status=405)
