import uuid

import pytest

from kttk import path_cache_manager
from kttk.context import Context
from kttk.path_cache_manager import PathCacheManager
from tests.fixtures.repository_fixtures import mongo_path_entry_repository


@pytest.fixture
def context_for_testing(ktrack_instance):
    project = ktrack_instance.create("project", {"name": "my_lovely_project"})
    return Context(project=project)


def test_good_path():
    path = r"\\stststr\<sr/sersear//ser"
    expected_path = r"/stststr/<sr/sersear/ser"

    actual_path = path_cache_manager.__good_path(path)

    assert actual_path == expected_path


class TestPathCacheManager(object):
    @pytest.fixture(autouse=True)
    def setup_path_cache_manager(self, mongo_path_entry_repository):
        self._mongo_path_entry_repository = mongo_path_entry_repository
        self._path_cache_manager = PathCacheManager(self._mongo_path_entry_repository)

    @pytest.mark.parametrize("path", [None, ""])
    def test_validate_path_is_valid(self, path):
        assert not self._path_cache_manager.is_valid_path(path)

    def test_validate_path_is_invalid(self):
        assert self._path_cache_manager.is_valid_path("my_path")

    @pytest.mark.parametrize("path,context", [(None, None), ("", None)])
    def test_register_invalid_path(self, path, context):
        with pytest.raises(ValueError):
            self._path_cache_manager.register_path(path, context)

    def test_register_path(self, context_for_testing):
        path = "nilascg"
        self._path_cache_manager.register_path(path, context_for_testing)

        assert self._mongo_path_entry_repository.find_by_path(path)

        context = self._path_cache_manager.context_from_path(path)
        assert context.project["id"] == context_for_testing.project["id"]

    def test_restore_context_no_path_registered(self):
        assert self._path_cache_manager.context_from_path(str(uuid.uuid4())) is None

    def test_unregister_path(self, context_for_testing):
        assert not self._path_cache_manager.unregister_path("sommovtrnitrui")

        PATH = "s<eihsdhisdi"
        self._path_cache_manager.register_path(PATH, context_for_testing)

        self._path_cache_manager.unregister_path(PATH)

        assert not self._mongo_path_entry_repository.find_by_path(PATH)
