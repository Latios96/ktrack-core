import re

from typing import Set, Dict


def find_all_tokens(template_str):
    # type: (str) -> Set[str]
    regex_matches = re.findall(r"{[^{, .}]*\}", template_str)
    all_tokens = {x[1:][:-1] for x in regex_matches}
    return all_tokens


def get_missing_tokens(string, token_dict):
    # type: (str, Dict[str, str]) -> Set[str]
    all_keys = find_all_tokens(string)

    provided_keys = set(token_dict)
    missing_keys = all_keys.difference(provided_keys)

    return missing_keys
