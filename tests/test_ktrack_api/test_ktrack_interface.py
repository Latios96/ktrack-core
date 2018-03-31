import mock
import pytest
from mock import MagicMock

from ktrack_api import ktrack
from ktrack_api.ktrack import Ktrack


@pytest.fixture
def ktrack_mocked_impl():
    impl_mock = MagicMock()
    kt = Ktrack(impl_mock)
    return kt, impl_mock


def test_create(ktrack_mocked_impl):
    kt, impl_mock = ktrack_mocked_impl
    assert kt._impl == impl_mock


def test_get_ktrack():
    with mock.patch("mongoengine.connect") as mock_mongo_impl:
        ktrack_instance = ktrack.get_ktrack()

        assert ktrack_instance._impl is not None


def test_ktrack_interface_create(ktrack_mocked_impl):
    kt, impl_mock = ktrack_mocked_impl

    kt.create("", {})
    assert impl_mock.create.called


def test_ktrack_interface_find(ktrack_mocked_impl):
    kt, impl_mock = ktrack_mocked_impl

    kt.find("", [])
    assert impl_mock.find.called


def test_ktrack_interface_find_one(ktrack_mocked_impl):
    kt, impl_mock = ktrack_mocked_impl

    kt.find_one("", "")
    assert impl_mock.find_one.called


def test_ktrack_interface_update(ktrack_mocked_impl):
    kt, impl_mock = ktrack_mocked_impl

    kt.update("", "", {})
    assert impl_mock.update.called


def test_ktrack_interface_delete(ktrack_mocked_impl):
    kt, impl_mock = ktrack_mocked_impl

    kt.delete("", "")
    assert impl_mock.delete.called
