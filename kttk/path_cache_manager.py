"""
Module providing path <-> Context functionality.
Sometimes we need to get the context from a path, for example the project from the current working directory.
For this, every folder created and deleted needs to be registered/unregistered in the database.
We store the path in the database together with the given context and can get the original context back with context_from_path
"""
import attr
from typing import Optional

from ktrack_api.factory import get_path_entry_repository
from ktrack_api.repositories import PathEntryRepository
from kttk.context import Context
from kttk.domain.entities import PathEntry


def _get_repo(path_entry_repository):
    return (
        get_path_entry_repository()
        if not path_entry_repository
        else path_entry_repository
    )


def register_path(path, context, path_entry_repository=None):
    # type: (str, Context, PathEntryRepository) -> dict
    if not is_valid_path(path):
        raise ValueError(path)

    path = __good_path(path)
    path_entry = PathEntry(path=path, context=context)  # todo remove user information

    path_entry_repository = _get_repo(path_entry_repository)
    return attr.asdict(path_entry_repository.save(path_entry))


def unregister_path(path, path_entry_repository=None):
    # type: (str,PathEntryRepository) -> bool
    path_entry_repository = _get_repo(path_entry_repository)
    path = __good_path(path)

    path_entry = path_entry_repository.find_by_path(path)
    if path_entry:
        path_entry_repository.delete(path_entry.id)
        return True
    else:
        return False


def context_from_path(path, path_entry_repository=None):
    # type: (str,PathEntryRepository) -> Optional[Context]
    path_entry_repository = _get_repo(path_entry_repository)
    path = __good_path(path)

    path_entry = path_entry_repository.find_by_path(path)
    if path_entry:
        return path_entry.context


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
