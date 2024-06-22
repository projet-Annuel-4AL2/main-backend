import time
from abc import abstractmethod, ABC
from .enums.language_implementation import Language


class Implementation(ABC):
    class Meta:
        abstract = True

    @abstractmethod
    def copy(self, container_name: str, source_path: str, dest_path='/tmp_code') -> None:
        pass

    @abstractmethod
    def run(self, language: Language, container_name: str):
        pass

    @abstractmethod
    def remove(self, container_name: str):
        pass

    @abstractmethod
    def exec(self, container_name: str):
        pass


class Runner:
    class Meta:
        container_number = 0

    def __init__(self, implementation: Implementation):
        self.implementation = implementation

    def _copy_source_files(self, container_name, source):
        self.implementation.copy(container_name, source)

    def _add_container(self, language: Language):
        container_name = f'{language.value}-container-{self.Meta.container_number}'
        container = self.implementation.run(language, container_name)
        self.Meta.container_number += 1

        return container

    def _delete_container(self, container_name: str):
        self.implementation.remove(container_name)

    def _execute(self, container_name: str):
        return self.implementation.exec(container_name)

    def execute_code(self, src_files_path: str, language: Language):
        container = self._add_container(language)
        container_name = container.name

        self._copy_source_files(container_name=container_name, source=src_files_path)

        exit_code, result = self._execute(container_name)

        self._delete_container(container_name)

        return exit_code, result
