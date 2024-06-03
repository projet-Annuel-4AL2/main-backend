from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess
import json




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
