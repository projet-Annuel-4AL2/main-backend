import json
import os
import shutil
import tempfile
from typing import Any
import uuid

from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from ..container import Container
from ..docker_implementation import DockerImplementation
from ..enums.language_implementation import Language
from ..runner import Runner


@method_decorator(csrf_exempt, name='dispatch')
class PipelineView(View):
    @classmethod
    def _create_temp_files(cls, containers_json: list[dict[str, Any]], runner: Runner, pipeline_id: uuid.UUID):
        def has_input_file(json_file_data):
            return json_file_data is not None \
                   and json_file_data['name'] != "" \
                   and json_file_data['content'] != ""

        for container_data in containers_json:
            code = container_data.get('code')
            file_data = container_data.get('inputFile')
            language = container_data.get('language')

            try:
                language_enum_value = Language.from_str(language)
                container_data['language'] = language_enum_value
            except ValueError:
                return JsonResponse({'error': 'Either language name incorrect or language not yet implemented'},
                                    status=400)

            with tempfile.NamedTemporaryFile('wt', suffix='.py', encoding='utf8') as src_file:
                src_file.write(code)
                src_file.flush()

                container_data['srcCodePath'] = src_file.name
                del container_data['code']
                if has_input_file(file_data):
                    with tempfile.NamedTemporaryFile('wt') as inputFile:
                        inputFile.write(file_data['content'])
                        temp_dir_name = os.path.dirname(inputFile.name)
                        shutil.move(inputFile.name, os.path.join(temp_dir_name, file_data['name']))
                        inputFile.name = os.path.join(temp_dir_name, file_data['name'])
                        inputFile.flush()

                        container_data['inputFilePath'] = inputFile.name
                        del container_data['inputFile']
                        container = Container.from_json(container_data)
                        runner.populate_pipeline(pipeline_id, [container])
                else:
                    if 'inputFile' in container_data:
                        del container_data['inputFile']
                    container = Container.from_json(container_data)
                    runner.populate_pipeline(pipeline_id, [container])

    def post(self, request: HttpRequest) -> JsonResponse:
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Format JSON invalide'}, status=400)

        if not isinstance(data, list):
            return JsonResponse({'error': 'Request body should contain a JSON list'}, status=400)

        runner = Runner(DockerImplementation())
        pipeline_id = runner.create_pipeline()
        error_response = self._create_temp_files(containers_json=data, runner=runner, pipeline_id=pipeline_id)

        if error_response is not None:
            return error_response

        execution_order, exit_code, output = runner.execute_pipeline(pipeline_id)

        return JsonResponse({'step_number': execution_order, 'exit_code': exit_code, 'output': output.decode()},
                            status=200)
