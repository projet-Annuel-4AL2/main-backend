from enum import StrEnum


class Language(StrEnum):
    PYTHON = 'python'
    PHP = 'php'

    @staticmethod
    def from_str(language: str):
        try:
            return Language[language.upper()]
        except KeyError:
            raise ValueError(f'Invalid language string {str}')
