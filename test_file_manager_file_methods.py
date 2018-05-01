import os

import pytest
from mock import MagicMock, patch

from kttk import template_manager
from kttk.context import Context
from kttk.file_manager import FileManager, InvalidContextException, FILE_CREATION_MODE, FileCurrentlyOpened
from tests.test_ktrack_api.test_ktrack_api import ktrack_instance


@pytest.fixture
def mock_engine():
    # mock engine
    engine_mock = MagicMock()
    engine_mock.file_extension = ".mb"
    engine_mock.name = "Maya"
    return engine_mock


@pytest.fixture()
def file_manager(mock_engine):
    manager = FileManager()
    manager._engine = mock_engine
    return manager


@pytest.fixture
def populated_context():
    return Context(project={'name': 'my_project'},
                   entity={'type': 'asset', 'code': 'my_entity', 'asset_type': 'prop'},
                   step={'name': 'step'},
                   task={'name': 'task', 'id': 'some_id'},
                   workfile={'name': 'workfile', 'path': 'some_path', 'comment': 'awesome', 'version_number': 1},
                   user={'name': 'user'})

# todo one check for creation of create from exisiting / not exisiting

def test_create_has_scene_open_abort(file_manager, populated_context):
    """
    Should throw FileCurrentlyOpened exception as mode is ABORT
    :return:
    """
    # mock current_file_path
    file_manager._engine.current_file_path.return_value = "some_file_path"

    with pytest.raises(FileCurrentlyOpened):
        file_manager.create(populated_context, mode=FILE_CREATION_MODE.ABORT)


def test_create_has_scene_open_template_file_no_existing_workfile_no_unsaved_changes(file_manager, populated_context, ktrack_instance):
    """
    Scene open: yes
    Mode: USE_TEMPLATE
    Existing File: No
    Unsaved Changes: No
    Tests creation of a new file with no existing workfile, so a new one should be created
    Should throw FileCurrentlyOpened exception as mode is ABORT
    :return:
    """
    # mock methods on file manager
    file_manager._engine.current_file_path.return_value = "some_file_path"
    file_manager._engine.has_unsaved_changes.return_value = False
    file_manager._create_new_workfile = MagicMock()

    # mock database
    with patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance
        file_manager.create(populated_context, mode=FILE_CREATION_MODE.USE_TEMPLATE)

        # assert that template file was opened
        assert file_manager._engine.open_file_by_path.called

        # assert _create_new_workfile way called, because we have no existig workfile
        assert file_manager._create_new_workfile.called

        # assert save_as was called
        assert file_manager._engine.save_as.called

        # assert update_file_for_context was called
        assert file_manager._engine.update_file_for_context.called


def test_create_has_scene_open_template_file_existing_workfile_no_unsaved_changes(file_manager, populated_context, ktrack_instance):
    """
    Scene open: yes
    Mode: USE_TEMPLATE
    Existing File: Yes
    Unsaved Changes: No
    Tests creation of a new file with existing workfile, so a new one should be created from this workfile
    Should throw FileCurrentlyOpened exception as mode is ABORT
    :return:
    """
    # mock methods on file manager
    file_manager._engine.current_file_path.return_value = "some_file_path"
    file_manager._engine.has_unsaved_changes.return_value = False
    file_manager._create_new_workfile = MagicMock()
    file_manager._create_workfile_from = MagicMock()
    file_manager._get_highest_workfile = MagicMock()
    file_manager._get_highest_workfile.return_value = {'version_number': 2, 'type': 'workfile'}

    # mock database
    with patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance
        file_manager.create(populated_context, mode=FILE_CREATION_MODE.USE_TEMPLATE)

        # assert that template file was opened
        assert file_manager._engine.open_file_by_path.called

        # assert _create_new_workfile way called, because we have no existig workfile
        assert file_manager._create_workfile_from.called
        assert not file_manager._create_new_workfile.called

        # assert save_as was called
        assert file_manager._engine.save_as.called

        # assert update_file_for_context was called
        assert file_manager._engine.update_file_for_context.called


def test_has_scene_open_save_as_no_existing_no_unsaved_changes(file_manager, populated_context, ktrack_instance):
    """
    Scene open: yes
    Mode: SAVE_CURRENT_AS_NEW
    Existing File: No
    Unsaved Changes: No
    Tests creation of a new file with existing workfile, so a new one should be created from this workfile
    Will save current file as new file, so no open scene should be called
    :return:
    """
    # mock methods on file manager
    file_manager._engine.current_file_path.return_value = "some_file_path"
    file_manager._engine.has_unsaved_changes.return_value = False
    file_manager._create_new_workfile = MagicMock()
    file_manager._create_workfile_from = MagicMock()
    file_manager._get_highest_workfile = MagicMock()
    file_manager._get_highest_workfile.return_value = None

    # mock database
    with patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance
        file_manager.create(populated_context, mode=FILE_CREATION_MODE.SAVE_CURRENT_AS_NEW)

        # assert that template file was opened
        assert not file_manager._engine.open_file_by_path.called

        # assert _create_new_workfile way called, because we have no existig workfile
        assert file_manager._create_new_workfile.called

        # assert save_as was called
        assert file_manager._engine.save_as.called

        # assert update_file_for_context was called
        assert file_manager._engine.update_file_for_context.called


def test_has_no_scene_open_save_as_existing(file_manager, populated_context, ktrack_instance):
    """
    Scene open: No
    Mode: default, is not needed here, because we have no scene open, so we donthave to decide what to do with this
    Existing File: Yes
    Unsaved Changes: Not checked, got no scene open
    We have no scene file open, so we create a new one based on template
    :return:
    """
    # mock methods on file manager
    file_manager._engine.current_file_path.return_value = None
    file_manager._create_new_workfile = MagicMock()
    file_manager._create_workfile_from = MagicMock()
    file_manager._get_highest_workfile = MagicMock()
    file_manager._get_highest_workfile.return_value = None

    # mock database
    with patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance
        file_manager.create(populated_context)

        # assert that template file was opened
        assert file_manager._engine.open_file_by_path.called

        # assert _create_new_workfile way called, because we have no existig workfile
        assert file_manager._create_new_workfile.called

        # assert save_as was called
        assert file_manager._engine.save_as.called

        # assert update_file_for_context was called
        assert file_manager._engine.update_file_for_context.called
