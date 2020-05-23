from typing import Set, Optional, Dict

from kttk.naming_system.internal.templates import PathTemplate
from vendor import lucidity
from vendor.lucidity.template import Template


class NamingConfig(object):
    def __init__(self, path_templates):
        # type: (Set[PathTemplate]) -> None
        self._route_templates = path_templates
        self._route_template_dict = self._create_path_template_dict()

    def route_template_by_name(self, template_name):
        # type: (str) -> Optional[Template]
        return self._route_template_dict.get(template_name)

    def _create_path_template_dict(self):
        # type: () -> Dict[str, Template]
        path_template_dict = {}
        for template in self._route_templates:
            path_template_dict[template.name] = self._create_lucidity_template(
                template, path_template_dict
            )
        return path_template_dict

    def __eq__(self, other):
        # type: (NamingConfig) -> bool
        return self._route_templates == other._route_templates

    def __ne__(self, other):
        # type: (NamingConfig) -> bool
        return not self == other

    def __repr__(self):
        # type: () -> str
        return str(self)

    def __str__(self):
        # type: () -> str
        return "<NamingConfig route_templates={}".format(
            ", ".join(map(str, sorted(self._route_templates, key=lambda x: x.name)))
        )

    def _create_lucidity_template(self, template, path_template_dict):
        # type: (PathTemplate,Dict[str, Template]) -> Template
        lucidity_template = Template(template.name, template.template_str)
        lucidity_template.template_resolver = path_template_dict
        lucidity_template.duplicate_placeholder_mode = lucidity_template.STRICT
        return lucidity_template
