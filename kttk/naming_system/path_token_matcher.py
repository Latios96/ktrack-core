import re

import attr
from typing import List, Optional, Dict

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
        return string[len(self.value) :]

    def _do_match(self, string):
        # type: (str) -> Optional[str]
        if self.value and string.startswith(self.value):
            return self.value

        match = re.match(self.token.regex, string)
        if match:
            return match.group()


class PathTokenSequenceMatcher(object):
    _token_values_by_name = None  # type: Dict[str, str]
    _tokens = None  # type: List[MatcherToken]
    _strings = None  # type: List[str]
    _current_element = None  # type: str

    def __init__(self, tokens, string):
        # type: (List[PathToken], str) -> None
        self._tokens = list(map(lambda x: MatcherToken(token=x), tokens))
        self._strings = re.split("(/)", string)
        self._current_element = ""
        self._token_values_by_name = {}

    def matches(self):
        # type: () -> Optional[Dict[str, str]]
        for index, token in enumerate(self._tokens):
            self._fetch_next_element()
            if not self._current_element:
                return None

            self._get_token_value_if_known(token)

            if token.matches(self._current_element):
                if self._exact_match_required(index) and not token.matches_exactly(
                    self._current_element
                ):
                    return None
                self._current_element = token.save_value_and_trim(self._current_element)
                self._token_values_by_name[token.token.name] = token.value
            else:
                return None
        return self._token_values_by_name

    def _fetch_next_element(self):
        if not self._current_element and self._strings:
            self._current_element = self._strings.pop(0)

    def _exact_match_required(self, index):
        is_last_element = index == len(self._tokens) - 1
        next_element_is_folder_seperator = (
            index <= len(self._tokens) - 2
            and self._tokens[index + 1].token.type == "FOLDER_SEPERATOR"
        )

        if is_last_element or next_element_is_folder_seperator:
            return True

        return False

    def _get_token_value_if_known(self, token):
        # type: (MatcherToken) -> None
        token.value = self._token_values_by_name.get(token.token.name)
