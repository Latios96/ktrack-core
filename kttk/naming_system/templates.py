import attr
from enum import Enum
from typing import Union


class TokenType(Enum):
    FOLDER_SEPERATOR = "FOLDER_SEPERATOR"
    KNOWN_STRING = "KNOWN_STRING"
    STRING = "STRING"

    @staticmethod
    def from_str(string):
        if string == "FOLDER_SEPERATOR":
            return TokenType.FOLDER_SEPERATOR
        if string == "KNOWN_STRING":
            return TokenType.KNOWN_STRING
        if string == "STRING":
            return TokenType.STRING


PathTokenType = Union["FOLDER_SEPERATOR", "KNOWN_STRING", "STRING", TokenType]


@attr.s(frozen=True)
class PathToken(object):
    name = attr.ib()  # type: str
    type = attr.ib()  # type: PathTokenType
    regex = attr.ib()  # type: str


@attr.s(frozen=True)
class PathTemplate(object):
    name = attr.ib()  # type:str
    template_str = attr.ib()  # type:str
    expanded_template = attr.ib()  # type: str
