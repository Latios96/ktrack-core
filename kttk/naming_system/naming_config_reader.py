import six
import yaml
from typing import Dict

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
        if not yml_data:
            raise ValueError("could not load data from given string!")

        routes = yml_data.get("routes")

        if routes is None:
            raise ValueError('"routes" key missing in config!')

        if not isinstance(routes, dict):
            raise ValueError('routes section is not a dictionary!')

        for key, value in routes.items():
            if not isinstance(key, six.string_types) or not isinstance(value, six.string_types):
                raise ValueError('route is not a string-string mapping!')

        return RawConfig(routes=routes)


class RawConfigExpander(object):
    def __init__(self, raw_config):
        # type: (RawConfig) -> None
        self._raw_config = raw_config

    def expand(self):
        # type: () -> NamingConfig
        path_templates = set()
        for route_name, route_str in self._raw_config.routes.items():
            path_templates.add(
                PathTemplate(
                    name=route_name, template_str=route_str, expanded_template=route_str
                )
            )
        return NamingConfig(path_templates=path_templates)


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

        #naming_config_validator = NamingConfigValidator(naming_config)
        #naming_config_validator.validate()

        return naming_config
