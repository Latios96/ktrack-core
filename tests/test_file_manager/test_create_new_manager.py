import pytest
from mock import MagicMock

from kttk.context import Context
from kttk.file_manager.create_new_manager import CreateNewManager


@pytest.fixture
def populated_context():
    return Context(project={'name': 'my_project'},
                   entity={'type': 'asset', 'code': 'my_entity', 'asset_type': 'prop'},
                   step={'name': 'step'},
                   task={'name': 'task', 'id': 'some_id'},
                   workfile={'name': 'workfile', 'path': 'some_path', 'comment': 'awesome', 'version_number': 1},
                   user={'name': 'user'})


@pytest.fixture
def create_new_manager(populated_context):
    manager = CreateNewManager(MagicMock(), MagicMock(), populated_context)
    manager._helper = MagicMock()
    return manager


##################### TEST CONTROL FLOW ###########################
def test_no_scene_open(create_new_manager):
    """
    Has no scene open, so will create from template
    """
    # type: (CreateNewManager) -> object
    create_new_manager._engine.current_file_path.return_value = None

    create_new_manager._create_from_template = MagicMock()

    create_new_manager.do_it()

    assert create_new_manager._create_from_template.called


def test_scene_open_use_template_no_changes(create_new_manager):
    """
    Some scene without unsaved changes is open, use template is choosen.
    """
    create_new_manager._engine.current_file_path.return_value = 'some_path'
    create_new_manager._engine.has_unsaved_changes.return_value = False

    create_new_manager._view_callback_provider.ask_for_template_use.return_value = True

    create_new_manager._create_from_template = MagicMock()

    create_new_manager.do_it()

    assert create_new_manager._create_from_template.called


def test_scene_open_use_template_has_changes_save(create_new_manager):
    """
    Some scene with unsaved changes is open, use template is choosen. Changes are saved
    """
    create_new_manager._engine.current_file_path.return_value = 'some_path'
    create_new_manager._engine.has_unsaved_changes.return_value = True

    create_new_manager._view_callback_provider.ask_for_template_use.return_value = True
    create_new_manager._view_callback_provider.ask_for_save.return_value = True

    create_new_manager._create_from_template = MagicMock()

    create_new_manager.do_it()

    assert create_new_manager._create_from_template.called
    assert create_new_manager._engine.save.called


def test_scene_open_use_template_has_changes_no_save(create_new_manager):
    """
    Some scene with unsaved changes is open, use template is choosen. Changes are not saved
    """
    create_new_manager._engine.current_file_path.return_value = 'some_path'
    create_new_manager._engine.has_unsaved_changes.return_value = True

    create_new_manager._view_callback_provider.ask_for_template_use.return_value = True
    create_new_manager._view_callback_provider.ask_for_save.return_value = False

    create_new_manager._create_from_template = MagicMock()

    create_new_manager.do_it()

    assert create_new_manager._create_from_template.called
    assert not create_new_manager._engine.save.called


def test_scene_open_no_template(create_new_manager):
    """
    Some scene is open, save current as new is chosen.
    """
    create_new_manager._engine.current_file_path.return_value = 'some_path'

    create_new_manager._view_callback_provider.ask_for_template_use.return_value = False

    create_new_manager._create_from_template = MagicMock()
    create_new_manager._save_current_as_new = MagicMock()

    create_new_manager.do_it()

    assert not create_new_manager._create_from_template.called
    assert create_new_manager._save_current_as_new.called


##################### TEST ACTIONS ###########################

def test_create_from_template(create_new_manager):
    create_new_manager._save_current_as_new = MagicMock()

    create_new_manager._create_from_template()
    assert create_new_manager._helper._get_template_file_path.called
    assert create_new_manager._engine.open_file_by_path.called
    assert create_new_manager._save_current_as_new.called


def test_save_current_as_new_no_workfile(create_new_manager):
    """
    tests save current as new with no preexisting workfile
    """
    # mock highest workfile
    create_new_manager._helper._get_highest_workfile.return_value = None

    create_new_manager._update_context = MagicMock()

    create_new_manager._save_current_as_new()

    assert create_new_manager._helper._create_new_workfile.called
    assert not create_new_manager._helper._create_workfile_from.called
    assert create_new_manager._engine.save_as.called
    assert create_new_manager._update_context.called


def test_save_current_as_new_preexisting_workfile(create_new_manager):
    """
    tests save current as new with no preexisting workfile
    """
    # mock highest workfile
    create_new_manager._helper._get_highest_workfile.return_value = {'version_number': 1, 'type': 'workfile'}

    create_new_manager._update_context = MagicMock()

    create_new_manager._save_current_as_new()

    assert not create_new_manager._helper._create_new_workfile.called
    assert create_new_manager._helper._create_workfile_from.called
    assert create_new_manager._engine.save_as.called
    assert create_new_manager._update_context.called


def test__update_context(create_new_manager):
    create_new_manager._update_context()

    assert create_new_manager._engine.update_file_for_context.called
