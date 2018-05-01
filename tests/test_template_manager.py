import os
import pytest

from mock import patch

from kttk import template_manager


def test_get_template_dir():
    template_dir = template_manager.get_template_dir()

    assert template_dir

    TEST_PATH = 'test_path'

    with patch.dict(os.environ, {template_manager.KTRACK_TEMPLATE_DIR: TEST_PATH}):
        template_dir = template_manager.get_template_dir()

        assert template_dir == TEST_PATH


def test_load_folder_template():
    yml_data = {'asset':
        {'folders': {
            "{project_root}/{project_name}/Assets/{asset_type}/{asset_name}": [
                "{asset_name}_Textures",
                {'__file__': {'name': 'workspace.mel', 'content': 'test'}},
                {'out': [{
                    'playblast': ['test']
                }]}
            ]
        }
        }}
    with patch.object(template_manager, '_data_folders', yml_data) as mock_yml_data:
        folders = template_manager.get_folder_templates('asset')

    print folders

    assert len(folders) is 3

    # check file
    assert "{project_root}/{project_name}/Assets/{asset_type}/{asset_name}" in folders
    assert "{project_root}/{project_name}/Assets/{asset_type}/{asset_name}/{asset_name}_Textures" in folders
    assert "{project_root}/{project_name}/Assets/{asset_type}/{asset_name}/out/playblast/test" in folders


def test_load_folder_template_not_existing_entity():
    """
    Tests if a key error is thrown when trying to get templates for a non existing entity type
    """
    with pytest.raises(KeyError):
        template_manager.get_folder_templates('not_existing_entity')


def test_get_file_template():
    yml_data = {'asset':
        {'folders': {
            "{project_root}/{project_name}/Assets/{asset_type}/{asset_name}": [
                "{asset_name}_Textures",
                {'__file__': {'name': 'workspace.mel', 'content': 'some_awesome_content'}},
                {'out': [{
                    'playblast': ['test']
                }]}
            ]
        }
        }}
    with patch.object(template_manager, '_data_folders', yml_data) as mock_yml_data:
        files = template_manager.get_file_templates('asset')

    print files

    assert len(files) is 1

    file_template = files[0]

    assert len(file_template.keys()) == 2
    assert 'content' in file_template.keys()
    assert 'path' in file_template.keys()

    assert file_template['path'] == "{project_root}/{project_name}/Assets/{asset_type}/{asset_name}/workspace.mel"

    assert file_template['content'] == "some_awesome_content"


def test_format_template():
    """
    Tests if format template works correctly
    """
    context = {'project_root': '/mnt/media/active/{year}',
               'project_name': 'awesome_project',
               'asset_type': 'Prop',
               'asset_name': 'my_awesome_asset',
               'year': 2018}

    template = "{project_root}/{project_name}/Assets/{asset_type}/{asset_name}/workspace.mel"

    formated_template = template_manager.format_template(template, context)
    print formated_template

    assert "{" not in formated_template

    assert formated_template == "/mnt/media/active/2018/awesome_project/Assets/Prop/my_awesome_asset/workspace.mel"


def test_not_all_tokens_provided():
    """
    Tests if KeyError is raised when not all tokens are supplied in context
    """

    template = "{my_awesome__token}"

    with pytest.raises(KeyError):
        formated_template = template_manager.format_template(template)

    with pytest.raises(KeyError):
        formated_template = template_manager.format_template(template, context_dict={'useless_key': 'some_value'})


def test_format_template_default_tokens():
    """
    Tests if default tokens provided by format_template are working correctly
    """

    # no context provided
    template = "{year}{platform}{hour}{minute}{second}{user}"

    formated_template = template_manager.format_template(template)

    for token in ['year', 'platform', 'hour', 'minute', 'second', 'user']:
        assert token not in formated_template

    # context provided, overrides some default values

    context = {'year': 2019}

    formated_template = template_manager.format_template(template, context_dict=context)

    assert formated_template.startswith("2019")


def test_format_tempate_version_number():
    template = "{version}"

    formated_template = template_manager.format_template(template, {'version': 1})

    assert formated_template == "v001"


def test_route_template():
    yml_data = {'project_root': 'somewhere_over_the_rainbow'}

    with patch.object(template_manager, '_data_routes', yml_data) as mock_yml_data:
        project_root = template_manager.get_route_template('project_root')

        assert project_root is not None

        with pytest.raises(template_manager.RouteNotExists):
            template_manager.get_route_template('this route does not exist')
