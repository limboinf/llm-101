"""
constant sets
"""
from enum import Enum


class FileType(Enum):
    """file type"""
    FILE = 0
    FOLDER = 1
    UNKNOWN = 2


class FileSuffix(Enum):
    """file suffix"""
    TXT = 'txt'
    PDF = "pdf"
    DOC = "doc"
    DOCS = "docx"
    HTML = "html"

    @staticmethod
    def to_file_suffix(s: str):
        try:
            return FileSuffix(s.lower())
        except ValueError:
            raise ValueError(f"{s} is not a valid file suffix")


    def __str__(self):
        return self.value


