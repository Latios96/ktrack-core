import json
import os
import sys

import ktrack_api

KTRACK_USER_JSON = ".ktrack_user.json"

# todo make sure this is the semantic: user_information: dict with type and id, user: complete user entity

def restore_user():
    """
    Returns information about current user, will use ~/.ktrack_user.json for this. If no user information is avaible, it will be created
    :return: dict like {'type': 'user, 'id': 'asdf'}
    """
    # check if ~/.ktrack_user.json exists at location
    user_information_path = get_user_information_path()

    # check if exists
    if os.path.isfile(user_information_path):
        with open(user_information_path, "r") as f:
            data = json.load(f)
        # validate data

        data_is_valid = data.get("type") and data.get("id")

        if data_is_valid:
            # return fresh dict, maybe someone has saved useless stuff in the dict
            return {'type': 'user', 'id': data['id']}

    # no information is avaible, so create it
    user = create_user()

    # we need to save it, since create_user can also be used to create a user for another machine. But when restoring we
    # want it on the same maschine

    save_user_information(user)

    return user


def get_user_information_path():
    """
    Returns the expanded path to ~/.ktrack_user.json
    :return: the expanded path to ~/.ktrack_user.json
    """
    is_windows = sys.platform.startswith('win')
    username = os.environ["username"] if is_windows else os.path.expanduser("~")
    user_folder = "C:/Users/{username}".format(username=username)

    user_information = os.path.join(user_folder, KTRACK_USER_JSON)
    return user_information


def save_user_information(user_information):
    """
    Saves information about given user to ~/KTRACK_USER_JSON
    :param user: user_information to save, dict like {'type': 'user, 'id': 'asdf'}
    :return:
    """
    user_information_path = get_user_information_path()

    data = {'type': 'user', 'id': user_information['id']}

    with open(user_information_path, "w") as f:
        json.dump(data, f)


def generate_user_name(first_name, second_name):
    # type: (str, str) -> str

    first_name_part = None
    second_name_part = None

    #  first name
    if first_name:
        if len(first_name) > 0:
            first_name_part = first_name[:1].lower()

    #  second name
    if second_name:
        if len(second_name) > 0:
            second_name_part = second_name[:1].upper() + second_name[1:].lower()

    # check if both where valid ( first_name_part and second_name_part are not None anymore)
    if first_name_part and second_name_part:
        return first_name_part + second_name_part

    # else at least one of them was None, check if it was second_name
    elif first_name_part:
        return first_name.lower()

    # else at least one of them was None, check if it was first_name
    elif second_name_part:
        return second_name.lower()

    # both were None
    return None


def create_user():
    # type: () -> dict
    """
    Queries first and second name from user, creates a new user. Does NOT save it to disk, as we may create a user for another PC
    :return: user_information of newly created user
    """
    # todo do command line version and PySide Gui Version
    # ask for first name
    first_name = raw_input("Enter first name: ")

    # ask for second name
    second_name = raw_input("Enter second name: ")

    # genereate user name
    username = generate_user_name(first_name, second_name)

    # todo check if user name if unique

    # create user in db
    kt = ktrack_api.get_ktrack()

    user = kt.create("user", {'name': username, 'first_name': first_name, 'second_name': second_name})
    user_information = {'type': 'user', 'id': user['id']}

    # return user information
    return user_information
