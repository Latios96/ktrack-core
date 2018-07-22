import pytest
from mock import MagicMock

from kttk.context import Context
from kttk.engines.abstract_engine import AbstractEngine


@pytest.fixture
def abstract_engine():
    return AbstractEngine()


def test_open_file(abstract_engine):
    change_file_mock = MagicMock()
    abstract_engine.change_file = change_file_mock

    file_to_open = {}
    abstract_engine.open_file(file_to_open)

    assert change_file_mock.assert_called


def test_save_as(abstract_engine):
    change_file_mock = MagicMock()
    abstract_engine.change_file = change_file_mock

    file_to_save_to = {}
    abstract_engine.save_as(file_to_save_to)

    assert change_file_mock.assert_called


def test_change_file(abstract_engine, populated_context):
    file_to_open = populated_context.workfile
    abstract_engine.open_file(file_to_open)

    # todo we need to ignore user here, because we have no good way at the moment, because we cant simply use restore_user
    assert abstract_engine.context == populated_context.copy_context(user=None)


def test_current_workfile(abstract_engine):
    abstract_engine.context = Context(workfile='some_file')

    assert abstract_engine.current_workfile == 'some_file'
