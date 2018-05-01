import pytest
from mock import MagicMock, patch

from kttk.context import Context
from kttk.file_manager.file_manager import FileManager


@pytest.fixture
def populated_context():
    return Context(project={'name': 'my_project'},
                   entity={'type': 'asset', 'code': 'my_entity', 'asset_type': 'prop'},
                   step={'name': 'step'},
                   task={'name': 'task', 'id': 'some_id'},
                   workfile={'name': 'workfile', 'path': 'some_path', 'comment': 'awesome', 'version_number': 1},
                   user={'name': 'user'})


@pytest.fixture
def file_manager():
    manager = FileManager(MagicMock())
    manager._engine = MagicMock()
    return manager


def test_create_new(file_manager, populated_context):
    with patch('kttk.file_manager.create_new_manager.CreateNewManager.do_it') as mock_do_it:
        file_manager.create(populated_context)

        assert  mock_do_it.called
