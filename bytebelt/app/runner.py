from abc import abstractmethod, ABC
from .enums.language_implementation import Language
import os
import queue
import shutil
import tempfile
import uuid

from .container import Container


class Implementation(ABC):
    class Meta:
        abstract = True

    @abstractmethod
    def copy(self, container_name: str, source_path: str, dest_path='/tmp_code') -> None:
        pass

    @abstractmethod
    def start(self, language: Language, container_name: str):
        pass

    @abstractmethod
    def remove(self, container_name: str):
        pass

    @abstractmethod
    def exec(self, container_name: str):
        pass


class Runner(object):
    class Meta:
        container_number = 0
        instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.Meta.instance:
            cls.Meta.instance = super(Runner, cls).__new__(cls)
        return cls.Meta.instance

    def __init__(self, implementation: Implementation):
        self.implementation: Implementation = implementation
        self.pipelines: dict[uuid.UUID, queue.PriorityQueue] = {}

    def _copy_files(self, container_name, src_path):
        self.implementation.copy(container_name, src_path)

    def _add_container(self, language: Language):
        container_name = f'{language.value}-container-{self.Meta.container_number}'
        container = self.implementation.start(language, container_name)
        self.Meta.container_number += 1

        return container

    def _delete_container(self, container_name: str):
        self.implementation.remove(container_name)

    def _execute(self, container_name: str):
        return self.implementation.exec(container_name)

    def _setup(self, src_files_path: str, language: Language, input_files_path: str = None) -> str:
        container = self._add_container(language)
        container_name = container.name

        self._copy_files(container_name=container_name, src_path=src_files_path)

        if input_files_path is not None:
            self._copy_files(container_name=container_name, src_path=input_files_path)

        return container_name

    def execute_single_container(self, src_files_path: str, language: Language, input_files_path: str = None):
        container_name = self._setup(src_files_path, language, input_files_path)

        return self._execute_code(container_name)

    def _execute_code(self, container_name: str):
        try:
            exit_code, result = self._execute(container_name)
        except Exception:
            raise Exception
        finally:
            self._delete_container(container_name)

        return exit_code, result

    def create_pipeline(self) -> uuid.UUID:
        pipeline_id = uuid.uuid4()
        self.pipelines[pipeline_id] = queue.PriorityQueue()

        return pipeline_id

    def populate_pipeline(self, pipeline_id: uuid.UUID, containers: list[Container]):
        pipeline = self.pipelines[pipeline_id]

        for container in containers:
            container.name = self._setup(container.src_code_path, container.language, container.input_file_path)
            pipeline.put((container.execution_order, container))

    def execute_pipeline(self, pipeline_id: uuid.UUID):
        pipeline = self.pipelines[pipeline_id]

        execution_order, container = pipeline.get()
        while not pipeline.empty():
            exit_code, result = self._execute_code(container.name)

            if exit_code != 0:
                del self.pipelines[pipeline_id]
                return execution_order, exit_code, result

            with tempfile.NamedTemporaryFile('wt') as outputFile:
                outputFile.write(result.decode())
                temp_dir_name = os.path.dirname(outputFile.name)
                shutil.move(outputFile.name, os.path.join(temp_dir_name, container.output_file_name))
                outputFile.name = os.path.join(temp_dir_name, container.output_file_name)
                outputFile.flush()
                execution_order, container = pipeline.get()
                self._copy_files(container.name, outputFile.name)

        exit_code, result = self._execute_code(container.name)

        return execution_order, exit_code, result
