from typing import Set, Optional, Dict

from kttk.naming_system.templates import PathTemplate


class NamingConfig(object):
    def __init__(self, path_templates):
        # type: (Set[PathTemplate]) -> None
        self._path_templates = path_templates
        self._path_template_dict = self._create_path_template_dict()

    def path_template_by_name(self, template_name):
        # type: (str) -> Optional[PathTemplate]
        return self._path_template_dict.get(template_name)

    def _create_path_template_dict(self):
        # type: () -> Dict[str, PathTemplate]
        path_template_dict = {}
        for template in self._path_templates:
            path_template_dict[template.name] = template
        return path_template_dict

    def __eq__(self, other):
        return self._path_templates == other._path_templates

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "<NamingConfig path_templates={}".format(", ".join(map(str, sorted(self._path_templates, key=lambda x: x.name))))
