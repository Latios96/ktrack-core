import uuid

import pytest

from kttk import path_cache_manager
from kttk.context import Context


@pytest.fixture
def context_for_testing(ktrack_instance):
    project = ktrack_instance.create("project", {"name": "my_lovely_project"})
    return Context(project=project)


def test_validate_path():
    # check None
    assert not path_cache_manager.is_valid_path(None)

    assert not path_cache_manager.is_valid_path("")

    assert path_cache_manager.is_valid_path("my_path")


def test_good_path():
    path = r"\\stststr\<sr/sersear//ser"
    expected_path = r"/stststr/<sr/sersear/ser"

    actual_path = path_cache_manager.__good_path(path)

    assert actual_path == expected_path


def test_register_invalid_path():
    with pytest.raises(ValueError):
        path_cache_manager.register_path(None, None)

    with pytest.raises(ValueError):
        path_cache_manager.register_path("", None)


def test_register_path(mongo_path_entry_repository, context_for_testing):
    path = "nilascg"
    path_cache_manager.register_path(
        path, context_for_testing, mongo_path_entry_repository
    )

    assert mongo_path_entry_repository.find_by_path(path)

    context = path_cache_manager.context_from_path(path, mongo_path_entry_repository)
    assert context.project["id"] == context_for_testing.project["id"]


def test_restore_context_no_path_registered(mongo_path_entry_repository):
    assert (
        path_cache_manager.context_from_path(
            str(uuid.uuid4()), mongo_path_entry_repository
        )
        is None
    )


def test_unregister_path(context_for_testing, mongo_path_entry_repository):
    assert not path_cache_manager.unregister_path(
        "sommovtrnitrui", mongo_path_entry_repository
    )

    PATH = "s<eihsdhisdi"
    path_cache_manager.register_path(
        PATH, context_for_testing, mongo_path_entry_repository
    )

    path_cache_manager.unregister_path(PATH, mongo_path_entry_repository)

    assert not mongo_path_entry_repository.find_by_path(PATH)
