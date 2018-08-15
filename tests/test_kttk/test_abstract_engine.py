import pytest
from mock import MagicMock, mock

from kttk.context import Context
from kttk.engines.abstract_engine import AbstractEngine


@pytest.fixture
def abstract_engine():
    return AbstractEngine()


def test_open_file(abstract_engine, workfile_dict):
    # change file should be called

    change_file_mock = MagicMock()
    abstract_engine.change_file = change_file_mock

    file_to_open = workfile_dict
    abstract_engine.open_file(file_to_open)

    assert change_file_mock.assert_called


def test_save_as(abstract_engine, workfile_dict):
    # change file should be called

    change_file_mock = MagicMock()
    abstract_engine.change_file = change_file_mock

    file_to_save_to = workfile_dict
    abstract_engine.save_as(file_to_save_to)

    assert change_file_mock.assert_called


def test_change_file(abstract_engine, populated_context, ktrack_instance):
    # context should be changed to the context of the file to open
    file_to_open = populated_context.workfile
    abstract_engine.change_file(file_to_open)

    # todo we need to ignore user here, because we have no good way at the moment, because we cant simply use restore_user
    assert abstract_engine.context == populated_context.copy_context(user=None)


def test_current_workfile(abstract_engine, workfile_dict):
    abstract_engine.context = Context(workfile=workfile_dict)

    assert abstract_engine.current_workfile == {'type': 'workfile', 'id': workfile_dict['id']}


def test_update_file_for_context(abstract_engine):
    with mock.patch('kttk.engines.abstract_engine.AbstractEngine.serialize_context_to_file') as mock_serialize:
        abstract_engine.update_file_for_context()
        assert mock_serialize.called
