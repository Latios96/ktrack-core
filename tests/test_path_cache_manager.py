import uuid

import pytest

from kttk import path_cache_manager
from kttk.context import Context


@pytest.fixture
def context_for_testing(ktrack_instance):
    project = ktrack_instance.create("project", {'name': 'my_lovely_project'})
    return Context(project=project)


def test_good_path():
    path = r"\\stststr\<sr/sersear//ser"
    expected_path = r"/stststr/<sr/sersear/ser"

    actual_path = path_cache_manager.__good_path(path)

    assert actual_path == expected_path


def test_register_path(ktrack_instance, context_for_testing):
    PATH = 'nilascg'
    path_cache_manager.register_path(PATH, context_for_testing)

    entries = ktrack_instance.find('path_entry', [['path', 'is', PATH]])

    path_entry_exists = len(entries) == 1
    assert path_entry_exists

    # test restoring context from path

    context = path_cache_manager.context_from_path(PATH)

    assert context.project['id'] == context_for_testing.project['id']

def test_restore_context_no_path_registered():
    with pytest.raises(path_cache_manager.PathNotRegistered):
        path_cache_manager.context_from_path(str(uuid.uuid4()))

def test_unregister_path(context_for_testing, ktrack_instance):
    with pytest.raises(path_cache_manager.PathNotRegistered):
        path_cache_manager.unregister_path("sommovtrnitrui")

    PATH = "s<eihsdhisdi"
    path_cache_manager.register_path(PATH, context_for_testing)

    path_cache_manager.unregister_path(PATH)

    entries = ktrack_instance.find('path_entry', [['path', 'is', PATH]])

    path_entry_removed = len(entries) == 0
    assert path_entry_removed
