import re

import attr
from typing import List, Optional

from kttk.naming_system.templates import PathToken


@attr.s
class MatcherToken(object):
    token = attr.ib()  # type: PathToken
    value = attr.ib(default=None)  # type:str

    def matches(self, string):
        # type: (str) -> bool
        return self._do_match(string) is not None

    def matches_exactly(self, string):
        # type: (str) -> bool
        return self._do_match(string) == string

    def save_value_and_trim(self, string):
        # type: (str) -> str
        self.value = self._do_match(string)
        return string[len(self.value):]

    def _do_match(self, string):
        # type: (str) -> Optional[str]
        match = re.match(self.token.regex, string)
        if match:
            return match.group()


class PathTokenMatcher(object):

    def __init__(self, tokens, string):
        # type: (List[PathToken], str) -> None
        self._tokens = map(lambda x: MatcherToken(token=x), tokens)
        self._strings = re.split('(/)', string)
        self._current_element = None

    def matches(self):
        # type: () -> bool
        for token in self._tokens:
            self._fetch_next_element()

            if token.matches(self._current_element):
                if self._exact_match_required() and not token.matches_exactly(self._current_element):
                    return False
                self._current_element = token.save_value_and_trim(self._current_element)
            else:
                return False
        return True

    def _fetch_next_element(self):
        if not self._current_element:
            self._current_element = self._strings.pop(0)

    def _exact_match_required(self):
        is_last_element = len(self._tokens) == 1
        next_element_is_folder_seperator = len(self._tokens) >= 2 and self._tokens[1].token.type == 'FOLDER_SEPERATOR'

        if is_last_element or next_element_is_folder_seperator:
            return True

        return False
