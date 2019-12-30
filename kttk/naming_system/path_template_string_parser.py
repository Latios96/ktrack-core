import re

import attr
from typing import List

from kttk.naming_system.templates import PathTokenType, TokenType


@attr.s(frozen=True)
class ParsedPathToken(object):
    type = attr.ib()  # type: PathTokenType
    value = attr.ib()  # type: str


class PathTemplateStringParser(object):

    __compiled_token_regex = None

    def __init__(self, string):
        # type: (str) -> None
        self._string = string

    def parse(self):
        # type: () -> List[ParsedPathToken]
        return list(self._yield_tokens())

    def _yield_tokens(self):

        for mo in re.finditer(self._compiled_token_regex, self._string):
            token_type = mo.lastgroup
            value = mo.group()
            if value:
                yield ParsedPathToken(TokenType.from_str(token_type), value)

    @property
    def _compiled_token_regex(self):
        if not self.__compiled_token_regex:
            token_specification = [
                ("FOLDER_SEPERATOR", r"/"),
                ("STRING", r"{[^{, .}]*\}"),
                ("KNOWN_STRING", r"([^{/}]*)"),
            ]
            tok_regex = "|".join("(?P<%s>%s)" % pair for pair in token_specification)
            self.__compiled_token_regex = re.compile(tok_regex)
        return self.__compiled_token_regex
