import re

from typing import Set, Optional, Dict

from kttk.naming_system.templates import PathTemplate


class NamingConfig(object):
    def __init__(self, path_templates):
        # type: (Set[PathTemplate]) -> None
        self._path_templates = path_templates
        self._path_template_dict = self._create_path_template_dict()

    def path_template_by_name(self, template_name):
        # type: (str) -> Optional[PathTemplate]
        return self._path_template_dict.get(template_name)

    def _create_path_template_dict(self):
        # type: () -> Dict[str, PathTemplate]
        path_template_dict = {}
        for template in self._path_templates:
            path_template_dict[template.name] = template
        return path_template_dict


class NamingSystem(object):
    def __init__(self, naming_config):
        # type: (NamingConfig) -> None
        self._naming_config = naming_config

    def format_path_template(self, template_name, token_dict):
        path_template = self._naming_config.path_template_by_name(template_name)

        if not path_template:
            raise KeyError(
                "No template with name {} found in config!".format(template_name)
            )

        missing_tokens = self._get_missing_tokens(path_template, token_dict)
        if missing_tokens:
            raise ValueError(
                "Some tokens are missing: {}".format(", ".join(missing_tokens))
            )
        return path_template.expanded_template.format(**token_dict)

    def _get_missing_tokens(self, path_template, token_dict):
        # type: (PathTemplate, Dict[str, str]) -> Set[str]
        all_keys = {
            x[1:][:-1]
            for x in re.findall(r"{[^{, .]*\}", path_template.expanded_template)
        }
        provided_keys = set(token_dict)
        missing_keys = all_keys.difference(provided_keys)
        return missing_keys
