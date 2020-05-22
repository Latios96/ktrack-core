from typing import IO

from kttk.naming_system.internal.naming_config import NamingConfig
from kttk.naming_system.internal.raw_config_reader import RawConfigReader
from kttk.naming_system.internal.route_template_expander import RouteTemplateExpander


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
