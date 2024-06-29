import json
import tempfile

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .runner import Runner, Language
from .docker_implementation import DockerImplementation


@csrf_exempt
def execute_code(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            language = data.get('language')
            code = data.get('code')

            try:
                language_enum_value = Language.from_str(language)
            except ValueError:
                return JsonResponse(
                    {'error': 'Either language name incorrect or language not yet implemented'},
                    status=400
                )

            runner = Runner(DockerImplementation())
            with tempfile.NamedTemporaryFile('wt', suffix='.py', encoding='utf8') as file:
                file.write(code)
                file.flush()

                exit_code, output = runner.execute_code(file.name, language_enum_value)

            return JsonResponse({'exit_code': exit_code, 'output': output.decode()})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON invalide'}, status=400)

    return JsonResponse({'error': 'Unauthorized request method !@!'}, status=405)
