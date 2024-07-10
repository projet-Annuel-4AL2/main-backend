import time
from abc import abstractmethod, ABC
from dataclasses import dataclass
from .enums.language_implementation import Language
import json
from typing import Any
from re import sub
import uuid
import queue


def snake(s):
    return '_'.join(
        sub(r'([A-Z][a-z]+)', r' \1',
            sub(r'([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


@dataclass
class Container(object):
    name: str = None
    # or code
    src_code_path: str = None
    language: Language = None
    # or inputFile
    input_file_path: str = None
    execution_order: int = None

    @staticmethod
    def snake_keys_recursive(d: dict[str, Any]):
        if isinstance(d, dict):
            return {snake(key): Container.snake_keys_recursive(value) for key, value in d.items()}
        else:
            return d

    @classmethod
    def from_json(cls, json_kwargs: str | dict):
        if type(json_kwargs) == str:
            json_kwargs = json.loads(json_kwargs)
            assert type(json_kwargs) == dict, 'json_kwargs must be a dict or dict-like json formatted string'
        json_kwargs = Container.snake_keys_recursive(json_kwargs)

        return Container(**json_kwargs)


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
        exit_code, result = self._execute(container_name)
        self._delete_container(container_name)

        return exit_code, result

    def create_pipeline(self) -> uuid.UUID:
        pipeline_id = uuid.uuid4()
        self.pipelines[pipeline_id] = queue.PriorityQueue()

        return pipeline_id

    def populate_pipeline(self, pipeline_id, containers: list[Container]):
        pipeline = self.pipelines[pipeline_id]

        for container in containers:
            self._setup(container.src_code_path, container.language, container.input_file_path)
            pipeline.put((container.execution_order, container.src_code_path))
