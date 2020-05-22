import attr
import six
import yaml


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
