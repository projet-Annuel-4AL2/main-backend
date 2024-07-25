import io
import tarfile
import time

import docker
import os
from .enums.language_implementation import Language

from docker.models.containers import Container
from .runner import Implementation


class DockerImplementation(Implementation):
    TEMP_SRC_DIR_ABS_PATH = '/tmp_code/src/'

    def __init__(self):
        self.client = docker.from_env()
        self.containers = []

    def _find_container(self, container_name: str) -> Container | None:
        find_result = list(filter(lambda cont: cont.name == container_name, self.containers))

        if len(find_result) != 0:
            return find_result[0]
        else:
            return None

    @staticmethod
    def _create_temp_dir(container: Container, source_path: str, dest_path: str) -> str:
        # Create a temp directory for source code in container
        container.exec_run(['mkdir', dest_path])

        if os.path.isfile(source_path):
            dest_path = f'{dest_path}/src/'
            container.exec_run(['mkdir', dest_path])

        return dest_path

    def copy(self, container_name: str, source_path: str, dest_path='/tmp_code') -> None:
        if not os.path.exists(source_path):
            raise ValueError(f'Path {source_path} does not exist')

        container = self._find_container(container_name)
        if container is None:
            raise ValueError(f'Container {container_name} does not exist')

        dest_path = self._create_temp_dir(container, source_path, dest_path)

        # Creating a buffer to read tar binary data into memory
        with io.BytesIO() as buffer:
            with tarfile.open('temp.tar', mode='w') as tar:
                tar.fileobj = buffer
                if os.path.isdir(source_path):
                    tar.add(source_path, arcname='src')
                elif os.path.isfile(source_path):
                    tar.add(source_path, arcname=os.path.basename(source_path))
                folder_data = buffer.getvalue()

        container.put_archive(dest_path, folder_data)

    def start(self, language: Language, container_name: str):
        container = None
        # Command to keep the containers running
        initial_command = 'tail -f /dev/null'

        if not container_name.startswith(language.value):
            container_name = language.value + '-' + container_name

        common_config = {
            'command': initial_command,
            'detach': True,
            'name': container_name,
            'mem_limit': '1GB',
        }
        match language:
            case Language.PHP:
                container = self.client.containers.run(
                    image='php',
                    **common_config,
                )
            case Language.PYTHON:
                container = self.client.containers.run(
                    image='python',
                    **common_config,
                )
            case Language.JAVASCRIPT:
                container = self.client.containers.run(
                    image='node',
                    **common_config,
                )
            case Language.CPP:
                container = self.client.containers.run(
                    image='gcc',
                    **common_config,
                )
            case _:
                raise NotImplementedError(f'Runner for {language.value} is not implemented yet')

        self.containers.append(container)

        while container.status != 'running':
            container = self.client.containers.get(container.name)
            time.sleep(0.1)

        return container

    def remove(self, container_name: str):
        container = self._find_container(container_name)

        if container is None:
            raise ValueError(f'Container {container_name} does not exist')

        container.kill()
        container.remove()

    @classmethod
    def run_code(cls, container, container_name: str, filepath: str):
        execution_result = None

        if container_name.startswith(Language.PYTHON.value):
            execution_result = container.exec_run(['python', filepath], workdir=cls.TEMP_SRC_DIR_ABS_PATH)
        elif container_name.startswith(Language.PHP.value):
            execution_result = container.exec_run(['php', filepath], workdir=cls.TEMP_SRC_DIR_ABS_PATH)
        elif container_name.startswith(Language.JAVASCRIPT.value):
            execution_result = container.exec_run(['node', filepath], workdir=cls.TEMP_SRC_DIR_ABS_PATH)
        elif container_name.startswith(Language.CPP.value):
            result = container.exec_run(['g++', '-o', 'a.out', filepath], workdir=cls.TEMP_SRC_DIR_ABS_PATH)
            if result.exit_code != 0:
                return result
            execution_result = container.exec_run('./a.out', workdir=cls.TEMP_SRC_DIR_ABS_PATH)

        return execution_result

    @classmethod
    def _get_source_code_filename(cls, container) -> str:
        binary_output = container.exec_run(['ls', cls.TEMP_SRC_DIR_ABS_PATH]).output
        predicate = lambda fname: fname.endswith('.py') or fname.endswith('.js') or fname.endswith('.php') or fname.endswith('.cpp')

        return list(filter(predicate, binary_output.decode().strip().split('\n')))[0]

    def exec(self, container_name: str):
        container = self._find_container(container_name)

        if container is None:
            raise ValueError(f'Container {container_name} does not exist')

        source_file_name = self._get_source_code_filename(container)

        execution_result = self.run_code(container, container_name, f'{source_file_name}')

        return execution_result.exit_code, execution_result.output
