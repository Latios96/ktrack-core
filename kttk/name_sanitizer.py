# coding=utf-8
import re


def sanitize_name(entity_name):
    # type: (str) -> str
    """
    Makes project name beautifull and makes name conform to these rules:
    - no multiple underscores
    - no spaces
    - no characters, which are not allowed for folder names
    - german umlaute are replaced, ä -> ae
    :param entity_name: name of the project
    :return: name of the entity, conform to rules above
    """
    umlaute_mapping = {
        'ä': 'ae',
        'A': 'AE',
        'ö': 'oe',
        'Ö': 'OE',
        'ü': 'ue',
        'Ü': 'UE',
        'ß': 'ss'
    }
    not_allowed = '<>:.?/\\|* "\''

    project_name = entity_name.strip()

    # remove all chars, which are not allowed in folder names
    for char in not_allowed:
        project_name = project_name.replace(char, "_")

    # remove german umlaute
    for key, value in umlaute_mapping.items():
        project_name = project_name.replace(key, value)

    # remove multiple underscores
    project_name = re.sub("_{2,99}", "_", project_name)

    return project_name
