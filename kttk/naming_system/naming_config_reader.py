from collections import OrderedDict

import six
import yaml
from typing import Dict, IO, Set

from kttk.naming_system import token_utils
from kttk.naming_system.naming_config import NamingConfig
import attr

from kttk.naming_system.path_template_string_parser import PathTemplateStringParser
from kttk.naming_system.templates import PathTemplate, PathToken


@attr.s(frozen=True)
class RawConfig(object):
    routes = attr.ib()  # type: Dict[str,str]
    tokens = attr.ib(default=set())  # type: Set[PathToken]


class RawConfigReader(object):
    def __init__(self, config_str):
        # type: (str) -> None
        self._config_str = config_str

    def read(self):
        # type: () -> RawConfig
        yml_data = yaml.load(self._config_str, Loader=yaml.BaseLoader)

        self._check_empty_yml_data(yml_data)

        tokens = self._process_tokens(yml_data)
        routes = self._process_routes(yml_data)

        return RawConfig(routes=routes, tokens=tokens)

    def _process_tokens(self, yml_data):
        tokens = yml_data.get("tokens")

        self._check_missing_tokens_section(tokens)
        self._check_tokens_is_dict(tokens)
        return self._convert_to_path_tokens(tokens)

    def _check_tokens_is_dict(self, tokens):
        if not isinstance(tokens, list):
            raise ValueError("tokens section is not a list!")

    def _check_missing_tokens_section(self, tokens):
        if tokens is None:
            raise ValueError('"tokens" key missing in config!')

    def _convert_to_path_tokens(self, tokens):
        return set(map(self._to_path_token, tokens))

    def _to_path_token(self, path_token_dict):
        name = path_token_dict.get("name")
        token_type = path_token_dict.get("type")
        regex = path_token_dict.get("regex")

        regex, token_type = self._apply_optional_regex_token_type_rules(
            name, regex, token_type
        )
        self._check_token_attributes_are_strings(name, regex, token_type)

        return PathToken(name=name, type=token_type, regex=regex)

    def _check_token_attributes_are_strings(self, name, regex, token_type):
        if not isinstance(name, six.string_types):
            raise ValueError("token name has to be string, was {}".format(name))
        if not isinstance(token_type, six.string_types):
            raise ValueError("token type has to be string, was {}".format(token_type))
        if not isinstance(regex, six.string_types):
            raise ValueError("token regex has to be string, was {}".format(regex))

    def _apply_optional_regex_token_type_rules(self, name, regex, token_type):
        if name is None:
            raise ValueError("token name is missing!")
        if name is not None and token_type is not None and regex is None:
            raise ValueError("token regex is missing!")
        if name is not None and token_type is None and regex is None:
            token_type = "KNOWN_STRING"
            regex = name
        if name is not None and regex is not None and token_type is None:
            token_type = "STRING"
        return regex, token_type

    def _process_routes(self, yml_data):
        routes = yml_data.get("routes")
        self._check_missing_routes_section(routes)
        self._check_routes_is_dict(routes)
        self._check_routes_are_str_str_mappings(routes)
        return routes

    def _check_routes_are_str_str_mappings(self, routes):
        for key, value in routes.items():
            if not isinstance(key, six.string_types) or not isinstance(
                value, six.string_types
            ):
                raise ValueError("route is not a string-string mapping!")

    def _check_routes_is_dict(self, routes):
        if not isinstance(routes, dict):
            raise ValueError("routes section is not a dictionary!")

    def _check_missing_routes_section(self, routes):
        if routes is None:
            raise ValueError('"routes" key missing in config!')

    def _check_empty_yml_data(self, yml_data):
        if not yml_data:
            raise ValueError("could not load data from given string!")


class RawConfigExpander(object):
    def __init__(self, raw_config):
        # type: (RawConfig) -> None
        self._raw_config = raw_config

    def expand(self):
        # type: () -> NamingConfig
        path_templates = set()
        for route_name, template_str in self._raw_config.routes.items():
            path_templates.add(
                PathTemplate(
                    name=route_name,
                    template_str=template_str,
                    expanded_template=self._expand_template_str(
                        route_name, template_str
                    ),
                )
            )
        return NamingConfig(path_templates=path_templates)

    def _expand_template_str(self, name, template_str):
        all_tokens = token_utils.find_all_tokens(template_str)

        for token in all_tokens:
            if self._token_is_route(token):
                template_str = template_str.replace(
                    "{{{}}}".format(token),
                    self._expand_template_str(name, self._raw_config.routes.get(token)),
                )
        return template_str

    def _token_is_route(self, token):
        return self._raw_config.routes.get(token) is not None


class NamingConfigValidator(object):
    _naming_config = None  # type: NamingConfig

    def __init__(self, naming_config):
        # type: (NamingConfig) -> None
        self._naming_config = naming_config

    def validate(self):
        self._check_for_duplicated_path_template_names()
        self._check_for_expanded_duplicates()

        for path_template in self._naming_config.path_templates:
            self._validate_path_template(path_template)

    def _check_for_duplicated_path_template_names(self):
        path_template_names = set()

        for path_template in self._naming_config.path_templates:
            if not path_template.name in path_template_names:
                path_template_names.add(path_template.name)
            else:
                raise ValueError(
                    "Duplicated path template name: {}".format(path_template.name)
                )

    def _check_for_expanded_duplicates(self):
        expanded_strings = OrderedDict()

        for path_template in self._naming_config.path_templates:
            possible_duplicate = expanded_strings.get(path_template.expanded_template)
            if not possible_duplicate:
                expanded_strings[path_template.expanded_template] = path_template
            else:
                duplicate = possible_duplicate
                raise ValueError(
                    "PathTemplate with name {} expands to the same template string as PathTemplate with name {}".format(
                        path_template.name, duplicate.name
                    )
                )

    def _validate_path_template(self, path_template):
        parser = PathTemplateStringParser(path_template.expanded_template)
        token_sequence = parser.parse()

        self._ensure_every_string_token_exists(token_sequence)
        self._ensure_path_template_is_parsable(token_sequence)

    def _ensure_every_string_token_exists(self, token_sequence):
        pass

    def _ensure_path_template_is_parsable(self, token_sequence):
        pass


class NamingConfigReader(object):
    @staticmethod
    def read_from_file_path(file_path):
        # type: (str) -> NamingConfig
        with open(file_path, "rb") as f:
            return NamingConfigReader.read_from_file(f)

    @staticmethod
    def read_from_file(file):
        # type: (IO) -> NamingConfig
        return NamingConfigReader.read_from_string(file.read())

    @staticmethod
    def read_from_string(config_str):
        # type: (str) -> NamingConfig
        config_reader = NamingConfigReader(config_str)
        return config_reader.read()

    def __init__(self, config_str):
        self._config_str = config_str

    def read(self):
        # type: () -> NamingConfig
        raw_config_reader = RawConfigReader(self._config_str)
        raw_config = raw_config_reader.read()

        raw_config_expander = RawConfigExpander(raw_config)
        naming_config = raw_config_expander.expand()

        return naming_config
