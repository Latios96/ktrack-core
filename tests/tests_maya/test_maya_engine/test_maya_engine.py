import kttk

from kttk import template_manager
from kttk.context import Context
from kttk.file_manager import file_manager
from kttk.file_manager.view_callback_mixin import ViewCallbackMixin
from tests import integration_test_only
from tests.tests_maya.test_maya_engine import maya_only

import pytest
from mock import patch, MagicMock, mock
import os

try:
    print "loading Maya..."
    import pymel.core as pm
    import maya.cmds as cmds
    from kttk.engines.maya_engine import MayaEngine
except:
    pass

print "Maya loaded!"


@pytest.fixture
def empty_file():
    pm.newFile(force=True)


@pytest.fixture
def saved_file(tmpdir):
    pm.newFile(force=True)

    path = os.path.join(tmpdir.dirname, 'maya_test_scene.ma')

    pm.saveAs(path)
    return path


@pytest.fixture
def maya_engine():
    return MayaEngine()


@maya_only
def test_current_file_path_empty_scene(maya_engine, empty_file):
    assert maya_engine.current_file_path() is None


@maya_only
def test_current_file_path_saved_scene(maya_engine, saved_file):
    assert os.path.normpath(maya_engine.current_file_path()) == os.path.normpath(saved_file)


@maya_only
def test_open_file(maya_engine, workfile_dict, saved_file):
    pm.newFile(force=True)

    with mock.patch('kttk.engines.maya_engine.MayaEngine.change_file') as mock_change_file:
        # make sure workfile has a valid maya scene path
        workfile_dict['path'] = saved_file

        file_to_open = workfile_dict

        maya_engine.open_file(file_to_open)

        assert os.path.normpath(pm.sceneName()) == os.path.normpath(saved_file)
        mock_change_file.assert_called()


@maya_only
def test_unsaved_changes(maya_engine, empty_file):
    assert maya_engine.has_unsaved_changes() == False

    # do some changes
    pm.polyCube()

    assert maya_engine.has_unsaved_changes() == True


@maya_only
def test_save(maya_engine, saved_file):
    pm.polyCube()

    assert cmds.file(q=True, modified=True) == True
    maya_engine.save()
    assert cmds.file(q=True, modified=True) == False


@maya_only
def test_save_as(maya_engine, saved_file, workfile_dict):
    pm.polyCube()

    assert cmds.file(q=True, modified=True) == True

    with mock.patch('kttk.engines.maya_engine.MayaEngine.change_file') as mock_change_file:
        with mock.patch('kttk.engines.maya_engine.MayaEngine.update_file_for_context') as mock_update_file:
            name, ext = os.path.splitext(saved_file)
            path = name + "_test" + ext

            file_to_save_to = workfile_dict
            file_to_save_to['path'] = path

            maya_engine.save_as(file_to_save_to)
            assert cmds.file(q=True, modified=True) == False
            assert os.path.normpath(pm.sceneName()) == os.path.normpath(path)
            mock_change_file.assert_called()
            mock_update_file.assert_called()


@maya_only
def test_update_file_for_context(maya_engine, saved_file, populated_context, tmpdir):
    maya_engine.context = populated_context

    yml_data = {'project_root': tmpdir.dirname,
                'asset_maya_workspace_location': "{project_root}/{project_name}/Assets/{asset_type}/{code}/{code}_Maya/",
                'render_image_file_name': "<Layer>/{version}/<Scene>"}

    with patch.object(template_manager, '_data_routes', yml_data) as mock_yml_data:
        mock_get_vray = MagicMock()
        mock_vray_settings = MagicMock()
        mock_get_vray.return_value = mock_vray_settings
        maya_engine.__get_vray_settings = mock_get_vray

        expected_project_path = "{}/my_project/Assets/prop/my_entity/my_entity_Maya".format(tmpdir.dirname)
        os.makedirs(expected_project_path)

        maya_engine.update_file_for_context()

        assert os.path.normpath(pm.workspace(q=True, rd=True)) == os.path.normpath(expected_project_path)

        assert mock_get_vray.fileNamePrefix.set.assert_called


@maya_only
def test_context_serialization(maya_engine, empty_file, populated_context):
    # test if serialization is working correctly in generall

    maya_engine.context = populated_context
    maya_engine.serialize_context_to_file()

    restored_context = maya_engine.deserialize_context_from_file()

    assert populated_context == restored_context


@maya_only
def test_context_serialization_with_save(maya_engine, saved_file, populated_context):
    # test if serialization is working correctly in generall
    # save context
    maya_engine.context = populated_context
    maya_engine.serialize_context_to_file()

    # save file
    pm.saveFile()

    pm.newFile()
    pm.openFile(saved_file)

    restored_context = maya_engine.deserialize_context_from_file()

    assert populated_context == restored_context


@pytest.fixture
def running_maya_engine():
    import kttk
    from kttk.engines import maya_engine
    kttk.engines.start_engine(maya_engine.MayaEngine)


@maya_only
@integration_test_only
def test_create_file(running_maya_engine, bootstrapped_project_with_data, empty_file):
    """
    We start from an empty file, so file will be created from template
    """
    project, project_data = bootstrapped_project_with_data

    view_callback = ViewCallbackMixin()

    # start engine
    manager = file_manager.FileManager(view_callback)

    context = Context(project=project_data['project'],
                      entity=project_data['Hank'],
                      step=project_data['Hank_modelling']['step'],
                      task=project_data['Hank_modelling'])

    workfile = manager.create(context)

    # make sure file exists on disk
    path = "M:/Projekte/2018/Finding_Dory/Assets/character/Hank/Hank_Maya/Hank_modelling_modelling_v001.mb"
    assert os.path.exists(path)

    # make sure file is opened in maya
    assert os.path.normpath(pm.sceneName()) == os.path.normpath(path)

    # make sure context is set correctly
    file_context = kttk.engines.current_engine().context
    assert file_context == context.copy_context(workfile=workfile)
    assert file_context.workfile


@maya_only
@integration_test_only
def test_context_serialize_deserialize(running_maya_engine, bootstrapped_project_with_data, empty_file):
    project, project_data = bootstrapped_project_with_data

    context = Context(project=project_data['project'],
                      entity=project_data['Hank'],
                      step=project_data['Hank_modelling']['step'],
                      task=project_data['Hank_modelling'])

    # change context
    kttk.engines.current_engine().context = context

    # serialize context
    kttk.engines.current_engine().serialize_context_to_file()

    # deserialze context and make sure they are the same
    assert kttk.engines.current_engine().deserialize_context_from_file() == context

# todo make checking if current file is correct more easy
# todo make test render to check render output paths
# todo also for shots
