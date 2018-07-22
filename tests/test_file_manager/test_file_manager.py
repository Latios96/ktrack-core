import pytest
from mock import MagicMock, patch

from kttk.context import Context
from kttk.file_manager.file_manager import FileManager


@pytest.fixture
def file_manager():
    manager = FileManager(MagicMock())
    manager._engine = MagicMock()
    return manager


def test_create_new(file_manager, populated_context):
    with patch('kttk.file_manager.create_new_manager.CreateNewManager.do_it') as mock_do_it:
        file_manager.create(populated_context)

        assert  mock_do_it.called
