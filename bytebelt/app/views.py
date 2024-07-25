import json
import os.path
import tempfile
import shutil

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .runner import Runner, Language
from .docker_implementation import DockerImplementation


def has_input_file(json_file_data):
    return json_file_data is not None \
           and json_file_data['name'] is not None \
           and json_file_data['content'] is not None


def get_suffix(language: str) -> str:
    suffixes = {
        'python': '.py',
        'php': '.php',
        'javascript': '.js',
        'cpp': '.cpp',
    }
    return suffixes[language]


@csrf_exempt
def execute_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON invalide'}, status=400)

        if not isinstance(data, dict):
            return JsonResponse({'error': 'Request body should contain a JSON object'}, status=400)

        language = data.get('language')
        code = data.get('code')
        file_data = data.get('inputFile')

        try:
            language_enum_value = Language.from_str(language)
        except ValueError:
            return JsonResponse(
                {'error': 'Either language name incorrect or language not yet implemented'},
                status=400
            )

        runner = Runner(DockerImplementation())
        with tempfile.NamedTemporaryFile('wt', suffix=get_suffix(language), encoding='utf8') as file:
            file.write(code)
            file.flush()
            if has_input_file(file_data):
                with tempfile.NamedTemporaryFile('wt') as inputFile:
                    inputFile.write(file_data['content'])
                    temp_dir_name = os.path.dirname(inputFile.name)
                    shutil.move(inputFile.name, os.path.join(temp_dir_name, file_data['name']))
                    inputFile.name = os.path.join(temp_dir_name, file_data['name'])
                    inputFile.flush()

                    exit_code, output = runner.execute_single_container(file.name, language_enum_value, inputFile.name)
            else:
                exit_code, output = runner.execute_single_container(file.name, language_enum_value)

        return JsonResponse({'exit_code': exit_code, 'output': output.decode()})
    return JsonResponse({'error': 'Unauthorized request method !@!'}, status=405)
