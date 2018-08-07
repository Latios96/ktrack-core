import os

import yaml
import valideer
from typing import Callable, Tuple, Dict

KTRACK_TEMPLATE_DIR = 'KTRACK_TEMPLATE_DIR'

_general_data = None  # type: Dict[str, str]


class InvalidConfigException(Exception):

    def __init__(self, file_name, reason):
        super(InvalidConfigException, self).__init__("Error when loading config file {}: {}".format(file_name, reason))


def get_config_folder():
    # type: () -> str
    """
    Returns the path of the directory where the template files can be found.
    Default is dirname(__file__). Can be overriden by enviroment variable KTRACK_TEMPLATE_DIR
    :return: path of the directory where the template files can be found.
    """
    if KTRACK_TEMPLATE_DIR in os.environ.keys():
        return os.environ[KTRACK_TEMPLATE_DIR]
    else:
        return os.path.dirname(__file__)


def _validate_general_data(data):
    """
    Validates general.yml, is expected to be a dict of strings
    :param data: data to validate
    :return: (True, '') if valid, (False, reason) if not
    """
    schema = valideer.Mapping(key_schema=valideer.String, value_schema=valideer.String)
    try:
        schema.validate(data)
        return True, ''
    except valideer.ValidationError as e:
        return False, e.message


def _load_general_data():
    """
    Loads generall data and validates using _validate_general_data
    :return: loaded data
    """
    # load data
    return load_file('general.yml', _validate_general_data)


def get_value(key):
    # type: (str) -> str
    """
    Returns the config value from the given key specified in general.yml. Raises KeyError if there is no such key
    :param key:
    :return: value for key specified in general.yml.
    """
    global _general_data
    if not _general_data:
        _general_data = _load_general_data()

    return _general_data[key]


def load_file(yml_file_name, validator=None):
    # type: (str, Callable[[dict], Tuple[bool, str]]) -> dict
    """
    Loads the yml file with given name from config folder. Applies the given validator callable, if loaded data is not valid,
    InvalidConfigException is raised
    :param file_name:
    :param validator:
    :return: loaded data
    """
    yml_file_path = os.path.join(get_config_folder(), yml_file_name)
    # handle non-existing file
    if not os.path.exists(yml_file_path):
        raise InvalidConfigException(yml_file_name, "File does not exist!")

    # load data
    with open(yml_file_path) as file_descriptor:
        yml_data = yaml.load(file_descriptor)

    # apply validator

    if validator:
        is_valid, reason = validator(yml_data)

        if not is_valid:
            raise InvalidConfigException(yml_file_name, reason)

    return yml_data
