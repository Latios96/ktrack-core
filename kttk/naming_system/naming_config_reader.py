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


class RawConfigReader(object):
    def __init__(self, config_str):
        # type: (str) -> None
        self._config_str = config_str

    def read(self):
        # type: () -> RawConfig
        yml_data = yaml.load(self._config_str, Loader=yaml.BaseLoader)

        self._check_empty_yml_data(yml_data)

        routes = self._process_routes(yml_data)

        return RawConfig(routes=routes)

    def _check_empty_yml_data(self, yml_data):
        if not yml_data:
            raise ValueError("could not load data from given string!")

    def _process_routes(self, yml_data):
        routes = yml_data.get("routes")
        self._check_missing_routes_section(routes)
        self._check_routes_is_dict(routes)
        self._check_routes_are_str_str_mappings(routes)
        return self._join_routes(routes)

    def _check_missing_routes_section(self, routes):
        if routes is None:
            raise ValueError('"routes" key missing in config!')

    def _check_routes_is_dict(self, routes):
        if not isinstance(routes, dict):
            raise ValueError("routes section is not a dictionary!")

    def _check_routes_are_str_str_mappings(self, routes):
        for key, value in routes.items():
            if not isinstance(key, six.string_types):
                raise ValueError("route is not a string-string mapping!")

            if isinstance(value, dict):
                self._check_routes_are_str_str_mappings(value)
            elif not isinstance(value, six.string_types):
                raise ValueError("route is not a string-string mapping!")

    def _join_routes(self, routes, prefix=""):
        joined_routes = {}
        for key, value in routes.items():
            if isinstance(value, dict):
                joined_routes.update(
                    self._join_routes(value, prefix=self._add_prefix(prefix, key))
                )
            else:
                joined_routes[self._add_prefix(prefix, key)] = value
        return joined_routes

    def _add_prefix(self, prefix, key):
        if prefix:
            return "{}.{}".format(prefix, key)
        return key


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

        for path_template in self._naming_config.route_templates:
            self._validate_path_template(path_template)

    def _check_for_duplicated_path_template_names(self):
        path_template_names = set()

        for path_template in self._naming_config.route_templates:
            if not path_template.name in path_template_names:
                path_template_names.add(path_template.name)
            else:
                raise ValueError(
                    "Duplicated path template name: {}".format(path_template.name)
                )

    def _check_for_expanded_duplicates(self):
        expanded_strings = OrderedDict()

        for path_template in self._naming_config.route_templates:
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
