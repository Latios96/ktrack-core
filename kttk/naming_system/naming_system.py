from kttk.naming_system.internal.naming_config import NamingConfig
from kttk.naming_system.internal import token_utils


class NamingSystem(object):
    def __init__(self, naming_config):
        # type: (NamingConfig) -> None
        self._naming_config = naming_config

    def format_path_template(self, template_name, token_dict):
        path_template = self._naming_config.route_template_by_name(template_name)

        if not path_template:
            raise KeyError(
                "No template with name {} found in config!".format(template_name)
            )

        missing_tokens = token_utils.get_missing_tokens(
            path_template.expanded_pattern(), token_dict
        )
        if missing_tokens:
            raise ValueError(
                "Some tokens are missing: {}".format(", ".join(sorted(missing_tokens)))
            )
        return path_template.format(data=token_dict)
