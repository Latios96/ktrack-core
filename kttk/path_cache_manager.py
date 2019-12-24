"""
Module providing path <-> Context functionality.
Sometimes we need to get the context from a path, for example the project from the current working directory.
For this, every folder created and deleted needs to be registered/unregistered in the database.
We store the path in the database together with the given context and can get the original context back with context_from_path
"""
from typing import Optional

import ktrack_api
from kttk.context import Context


def register_path(path, context):
    # type: (str, Context) -> dict
    # check if path is valid
    if not is_valid_path(path):
        raise ValueError(path)

    path = __good_path(path)

    kt = ktrack_api.get_ktrack()

    path_entry_data = {}
    path_entry_data["path"] = path
    path_entry_data["context"] = context.as_dict()  # todo remove user information

    return kt.create("path_entry", path_entry_data)


def unregister_path(path):
    # type: (str) -> bool
    path = __good_path(path)

    kt = ktrack_api.get_ktrack()

    path_entries = kt.find("path_entry", [["path", "is", path]])

    entry_found = len(path_entries) > 0

    if entry_found:
        for path_entry in path_entries:
            kt.delete("path_entry", path_entry["id"])
        return True
    else:
        return False


def context_from_path(path):
    # type: (str) -> Optional[Context]
    path = __good_path(path)

    kt = ktrack_api.get_ktrack()

    context_dicts = kt.find("path_entry", [["path", "is", path]])
    context_found = len(context_dicts) > 0

    if context_found:
        context = Context.from_dict(context_dicts[0]["context"])
        return context
    else:
        return None


def is_valid_path(path):
    # type: (str) -> bool
    valid = False

    if path:
        if len(path) > 0:
            valid = True

    return valid


def __good_path(path):
    # type: (str) -> str
    path = path.replace("\\", "/")
    path = path.replace("//", "/")
    return path
