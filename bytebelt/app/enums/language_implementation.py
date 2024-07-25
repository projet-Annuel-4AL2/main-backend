from enum import StrEnum


class Language(StrEnum):
    PYTHON = 'python'
    PHP = 'php'
    JAVASCRIPT = 'javascript'
    CPP = 'cpp'

    @staticmethod
    def from_str(language: str):
        if language is None:
            raise ValueError(f'Language cannot be null')

        try:
            return Language[language.upper()]
        except KeyError:
            raise ValueError(f'Invalid language string {str}')
