import copy
import os

import pytest
from mock import patch

from kttk import folder_manager, template_manager


@pytest.fixture
def ktrack_project(ktrack_instance):
    """A project for testing"""
    project = ktrack_instance.create("project", {'name': 'My_Test_Project'})
    return project


def init_entity_test(ktrack_instance, tmpdir, entity, folders, files):
    """
    More abstract testing of test entity
    :return:
    """
    # we need to mock project root to something
    entity_type, entity_id = entity['type'], entity['id']

    # change project root
    mock_routes = copy.deepcopy(template_manager._data_routes)  # we take default routes and adjust what we need
    mock_routes['project_root'] = tmpdir.dirname

    # store old route length, so we can check if correct number of paths was created
    old_registered_paths = ktrack_instance.find("path_entry", [])
    old_len = len(old_registered_paths)

    with patch.object(template_manager, '_data_routes', mock_routes) as mock_yml_data:
        folder_manager.init_entity(entity_type, entity_id)

    # now verify that folders are created
    for folder in folders:
        folder = folder.format(project_root=tmpdir.dirname)
        assert os.path.exists(folder)

    for file_path in files:
        f = file_path.format(project_root=tmpdir.dirname)
        assert os.path.exists(f)

    # verify that folders are registered in database
    registered_paths = ktrack_instance.find("path_entry", [])
    new_len = len(registered_paths)
    assert new_len == old_len + len(folders) + len(files)


def test_init_project(ktrack_instance, ktrack_project, tmpdir):
    entity = ktrack_project

    folders = ['{project_root}/My_Test_Project',
               '{project_root}/My_Test_Project/Shots',
               '{project_root}/My_Test_Project/Assets']

    files = []

    init_entity_test(ktrack_instance, tmpdir, entity, folders, files)


def test_init_asset(ktrack_instance, ktrack_project, tmpdir):
    entity_data = {}
    entity_data['project'] = ktrack_project
    entity_data['code'] = 'Remote_Control'
    entity_data['asset_type'] = 'Prop'

    entity = ktrack_instance.create("asset", entity_data)

    folders = ['{project_root}/My_Test_Project/Assets/Prop/Remote_Control',
               '{project_root}/My_Test_Project/Assets/Prop/Remote_Control/Remote_Control_Textures',
               '{project_root}/My_Test_Project/Assets/Prop/Remote_Control/Remote_Control_Input_2D',
               '{project_root}/My_Test_Project/Assets/Prop/Remote_Control/Remote_Control_Input_3D',
               '{project_root}/My_Test_Project/Assets/Prop/Remote_Control/Remote_Control_Maya',
               '{project_root}/My_Test_Project/Assets/Prop/Remote_Control/Remote_Control_out',
               '{project_root}/My_Test_Project/Assets/Prop/Remote_Control/Remote_Control_out/playblast']

    files = ['{project_root}/My_Test_Project/Assets/Prop/Remote_Control/Remote_Control_Maya/workspace.mel']

    init_entity_test(ktrack_instance, tmpdir, entity, folders, files)

# todo tests for more entities
# todo test for entity with files
# todo test for entity which is not a project entity
