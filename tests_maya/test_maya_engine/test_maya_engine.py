from kttk import template_manager
from kttk.context import Context

print "loading Maya..."
import pymel.core as pm
import maya.cmds as cmds

print "Maya loaded!"

import pytest
from mock import patch, MagicMock
import os

from kttk.engines.maya_engine import MayaEngine


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


def test_current_file_path_empty_scene(maya_engine, empty_file):
    assert maya_engine.current_file_path() is None


def test_current_file_path_saved_scene(maya_engine, saved_file):
    assert os.path.normpath(maya_engine.current_file_path()) == os.path.normpath(saved_file)


def test_open_file(maya_engine, populated_context, saved_file):
    pm.newFile(force=True)

    # make sure workfile has a valid maya scene path
    populated_context.workfile['path'] = saved_file

    file_to_open = populated_context.workfile

    maya_engine.open_file(file_to_open)

    assert os.path.normpath(pm.sceneName()) == os.path.normpath(saved_file)


def test_unsaved_changes(maya_engine, empty_file):
    assert maya_engine.has_unsaved_changes() == False

    # do some changes
    pm.polyCube()

    assert maya_engine.has_unsaved_changes() == True


def test_save(maya_engine, saved_file):
    pm.polyCube()

    assert cmds.file(q=True, modified=True) == True
    maya_engine.save()
    assert cmds.file(q=True, modified=True) == False


def test_save_as(maya_engine, saved_file, populated_context):
    pm.polyCube()

    assert cmds.file(q=True, modified=True) == True

    name, ext = os.path.splitext(saved_file)
    path = name + "_test" + ext

    file_to_save_to = populated_context.workfile
    file_to_save_to['path'] = path

    maya_engine.save_as(file_to_save_to)
    assert cmds.file(q=True, modified=True) == False
    assert os.path.normpath(pm.sceneName()) == os.path.normpath(path)


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

        assert os.path.normpath(pm.workspace( q=True, rd=True)) == os.path.normpath(expected_project_path)

        assert mock_get_vray.fileNamePrefix.set.assert_called

# todo add tests for serialize / deserialize context