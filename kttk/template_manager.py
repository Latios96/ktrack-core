import copy
import getpass
import os
import platform
import re

import datetime

import valideer
import yaml

from kttk.config import config_manager

ROUTES_YML = 'routes.yml'

FOLDER_TEMPLATES_YML = 'folder_templates.yml'


class RouteNotExists(KeyError):

    def __init__(self, route_name):
        super(RouteNotExists, self).__init__(
            "Route with name {} does not exist! Please head over to {} and create your route!".format(route_name,
                                                                                                      os.path.join(
                                                                                                          config_manager.get_config_folder(),
                                                                                                          ROUTES_YML)))


def _validate_routes(route_data):
    """
    Validates route data, has to be Dict[str, str]
    :param route_data:
    :return: (True, '') if valid, (False, reason) if invalid
    """
    schema = valideer.Mapping(
        key_schema=valideer.String,
        value_schema=valideer.String)
    try:
        schema.validate(route_data)
        return True, ''
    except valideer.ValidationError as e:
        return False, e.message


# load data for folders
_data_folders = config_manager.load_file(FOLDER_TEMPLATES_YML, None)  # todo add validator

# load data for routes
_data_routes = config_manager.load_file(ROUTES_YML, _validate_routes)  # todo add validator


def get_file_templates(entity_type):
    # type: (str) -> list[dict[str, str]]
    """
    Returns a list of file templates for one entity.
    A file template is dictionary like this:
    {
        'path': 'path_template_with_{tokens},
        'content': 'file content woth {tokens}
    }
    :param entity_type: entity to get file templates for
    :return: a list of file templates
    """
    return get_file_and_folder_templates(entity_type)[0]


def get_folder_templates(entity_type):
    # type: (str) -> list[str]
    """
    Returns a list of folder templates for one entity. A folder template is a single string with {tokens}.
    Templates are configured in folder_templates.yml, in dirname(__file__) or in config_manager.KTRACK_TEMPLATE_DIR enviroment variable
    :param entity_type:
    :return:
    """
    return get_file_and_folder_templates(entity_type)[1]


def get_file_and_folder_templates(entity_type):
    # type: (str) -> tuple[list[dict[str, str]], list[str]]
    """
    Returns file and folder templates for given entity type
    :param entity_type: type of the entity as string
    :return: a tuple of a list of file templates and a list of folder templates
    """
    entity_type = entity_type.lower()

    if entity_type in _data_folders.keys():
        folder_data = _data_folders[entity_type.lower()]['folders']
    else:
        raise KeyError(
            "No templates found for entity type {}, please add them in folder_templates.yml".format(entity_type))

    all_folders = []
    all_files = []

    def iter_folders(folder_dict, parent=""):

        for parent_folder, subfolders in folder_dict.iteritems():
            parent_folder = parent + ("" if parent is "" else "/") + parent_folder
            for folder in subfolders:
                # folder dict
                if isinstance(folder, dict) and "__file__" not in folder.keys():
                    iter_folders(folder, parent=parent_folder)
                # file dict
                elif isinstance(folder, dict) and "__file__" in folder.keys():
                    # read values from config
                    file_path = "/".join([parent_folder, folder["__file__"]['name']])
                    file_content = folder["__file__"]['content']

                    # construct file template
                    file_template = {
                        'path': file_path,
                        'content': file_content}

                    all_files.append(file_template)

                    all_folders.append(os.path.dirname(file_path))

                # normal folder string
                else:
                    all_folders.append("/".join([parent_folder, folder]))

    iter_folders(folder_data)

    return all_files, all_folders


# todo add get_formatted_template, where we can pass route name and context and get formatted route
def get_route_template(route_name):
    # type: (str) -> str
    """
    Returns a route template, example would be project_root. route templates are strings
    :param route_name:
    :return:
    """
    try:
        route_template = _data_routes[route_name]
    except KeyError:
        raise RouteNotExists(route_name)
    return route_template


def get_all_route_templates():
    return copy.deepcopy(_data_routes)


def format_template(template, context_dict={}):
    # type: (str, dict) -> str
    """
    Takes a template string and replaces all tokens with values from context dictionary.
    Tokens in template string are in in {token_in_snake_case} format.
    The following tokens are provided by the function for you, so you don't have to provide them.
    If you provide these tokens, the default values are overridden.
    - year : current year, for example 2018
    - platform : current platform, Windows, Darwin or Linux
    - hour : current hour, for example 01
    - minute : current minute, for example 01
    - second : current second, for example 01
    - user : name of the current user, for example Jan
    :param template: the template string, containing tokens in {token_in_snake_case} format
    :param context_dict: dictionary containing all used tokens (or more) as keys and useful values.
    Example: {'asset_name': 'useful_value'}
    :return: the template string with all tokens replaced
    """

    current_time = datetime.datetime.now()

    default_context = {
        'year': current_time.year,
        'platform': platform.system(),
        'hour': current_time.hour,
        'minute': current_time.minute,
        'second': current_time.second,
        'user': getpass.getuser(),
        'config_root': os.path.join(os.path.dirname(__file__), 'config')
        # todo add test coverage for config_root default context
    }
    version_number = context_dict.get('version')
    if version_number:
        if isinstance(version_number, int):
            context_dict['version'] = "v{}".format("{}".format(version_number).zfill(3))

    # todo check if version is a token key and check if its in "v001" format
    default_context.update(context_dict)

    try:
        formated_template = template.format(**default_context)
        for i in range(5):
            formated_template = formated_template.format(**default_context)
    except KeyError:
        all_keys = {x[1:][:-1] for x in re.findall(r"\{[^\{, .]*\}", template)}
        provided_keys = set(default_context.keys())
        missing_keys = all_keys.difference(provided_keys)
        error_string = "Missing keys: {}".format(", ".join(list(missing_keys)))
        raise KeyError(error_string)

    return formated_template
