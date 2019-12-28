import six
import yaml
from typing import Dict

from kttk.naming_system import token_utils
from kttk.naming_system.naming_config import NamingConfig
import attr

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

        routes = yml_data.get("routes")

        self._check_missing_routes_section(routes)
        self._check_routes_is_dict(routes)
        self._check_routes_are_str_str_mappings(routes)

        return RawConfig(routes=routes)

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
    def __init__(self, naming_config):
        self._naming_config = naming_config

    def validate(self):
        raise NotImplementedError()


class NamingConfigReader(object):
    @staticmethod
    def read_from_file_path(file_path):
        with open(file_path, "rb") as f:
            return NamingConfigReader.read_from_file(file_path)

    @staticmethod
    def read_from_file(file):
        return NamingConfigReader.read_from_string(file.readall())

    @staticmethod
    def read_from_string(config_str):
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
