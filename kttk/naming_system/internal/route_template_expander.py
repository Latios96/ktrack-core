from kttk.naming_system.internal.naming_config import NamingConfig
from kttk.naming_system.internal.raw_config_reader import RawConfig
from kttk.naming_system.internal.templates import PathTemplate


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
