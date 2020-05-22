import datetime
import getpass
import os
import platform

from kttk.naming_system.internal.naming_config import NamingConfig
from kttk.naming_system.internal import token_utils


class NamingSystem(object):
    def __init__(self, naming_config):
        # type: (NamingConfig) -> None
        self._naming_config = naming_config

    def format_path_template(self, template_name, token_dict):
        tokens = self._create_default_tokens()
        tokens.update(token_dict)

        path_template = self._naming_config.route_template_by_name(template_name)

        if not path_template:
            raise KeyError(
                "No template with name {} found in config!".format(template_name)
            )

        missing_tokens = token_utils.get_missing_tokens(
            path_template.expanded_pattern(), tokens
        )
        if missing_tokens:
            raise ValueError(
                "Some tokens are missing: {}".format(", ".join(sorted(missing_tokens)))
            )
        return path_template.format(data=tokens)

    def _create_default_tokens(self):
        return self._stringify_dict({
            "current_date": self._current_date(),
            "config_root": os.path.join(
                os.path.dirname(os.path.dirname(__file__)), "config"
            ),
            "platform": self._current_platform(),
            "current_user": self._current_user(),
        })

    def _stringify_dict(self, dict_to_stringify):
        for key, value in dict_to_stringify.items():
            if isinstance(value, dict):
                self._stringify_dict(value)
            else:
                dict_to_stringify[key] = str(value)
        return dict_to_stringify

    def _current_date(self):
        current_time = datetime.datetime.now()

        return {
            "year": current_time.year,
            "hour": current_time.hour,
            "minute": current_time.minute,
            "second": current_time.second,
        }

    def _current_platform(self):
        return {"name": platform.system()}

    def _current_user(self):
        return {"name": getpass.getuser()}
