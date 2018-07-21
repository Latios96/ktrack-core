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


def test_change_file(abstract_engine):
    file_to_open = {}
    file_to_open['project'] = 'project'
    file_to_open['entity'] = {'step': 'anim', 'entity': 'shot'}
    abstract_engine.open_file(file_to_open)

    assert abstract_engine.context.project == 'project'
    assert abstract_engine.context.entity == 'shot'
    assert abstract_engine.context.step == 'anim'
    assert abstract_engine.context.task == {'step': 'anim', 'entity': 'shot'}
    assert abstract_engine.context.workfile == file_to_open


def test_current_workfile(abstract_engine):
    abstract_engine.context = Context(workfile='some_file')

    assert abstract_engine.current_workfile == 'some_file'
