from dataclasses import dataclass, field
import json
from typing import Any
from re import sub

from .enums.language_implementation import Language


def snake(s):
    return '_'.join(
        sub(r'([A-Z][a-z]+)', r' \1',
            sub(r'([A-Z]+)', r' \1',
                s.replace('-', ' '))).split()).lower()


@dataclass(order=True)
class Container(object):
    name: str = field(compare=False, default=None)
    src_code_path: str = field(compare=False, default=None)
    language: Language = field(compare=False, default=None)
    input_file_path: str = field(compare=False, default=None)
    execution_order: int = None
    output_file_name: str = field(compare=False, default=None)

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
