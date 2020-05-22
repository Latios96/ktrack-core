from typing import Dict, IO

import attr
import six
import yaml

from kttk.naming_system.naming_config import NamingConfig
from kttk.naming_system.templates import PathTemplate


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


class RouteTemplateExpander(object):
    def __init__(self, raw_config):
        # type: (RawConfig) -> None
        self._raw_config = raw_config

    def expand(self):
        # type: () -> NamingConfig
        path_templates = set()
        for route_name, template_str in self._raw_config.routes.items():
            path_templates.add(PathTemplate(name=route_name, template_str=template_str))
        return NamingConfig(path_templates=path_templates)


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

        raw_config_expander = RouteTemplateExpander(raw_config)
        naming_config = raw_config_expander.expand()

        return naming_config
