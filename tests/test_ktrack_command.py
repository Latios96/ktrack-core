import copy
import os
import uuid

import mock
import pytest
from mock import MagicMock

from kttk import template_manager
from kttk.context import Context
from kttk.path_cache_manager import PathNotRegistered
from scripts.ktrack_command import execute_cmd, NoAssetType
from tests.test_ktrack_api.test_ktrack_api import ktrack_instance

ASSET_NAME = 'my_test_asset'

PROJECT_NAME = 'my_mothafucking_project'


@pytest.fixture
def project_init_args():
    arg_mock = MagicMock()
    arg_mock.init = ['init', 'project', ('%s' % PROJECT_NAME)]

    return arg_mock


@pytest.fixture
def asset_init_args():
    arg_mock = MagicMock()
    arg_mock.init = ['init', 'asset', ASSET_NAME]
    arg_mock.asset_type = 'Prop'

    return arg_mock

@pytest.fixture
def asset_init_args_no_asset_type():
    arg_mock = MagicMock()
    arg_mock.init = ['init', 'asset', ASSET_NAME]
    arg_mock.asset_type = None
    return arg_mock


@pytest.fixture
def ktrack_registered_project(ktrack_instance):
    project_name = str(uuid.uuid4())
    project = ktrack_instance.create('project', {'name': project_name})

    context = Context(project=project)
    project_context_path = '/mnt/media/' + PROJECT_NAME
    ktrack_instance.create('path_entry', {'path': project_context_path, 'context': context.as_dict()})

    return project, project_context_path


def test_init_project(project_init_args, ktrack_instance):
    # mock get_ktrack

    with mock.patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        with mock.patch('kttk.init_entity') as mock_init_entity:
            mock_get_ktrack.return_value = ktrack_instance

            execute_cmd(project_init_args)

            # check project exists in DB
            projects_with_name = ktrack_instance.find('project', [['name', 'is', PROJECT_NAME]])
            only_one_project = len(projects_with_name) == 1

            assert only_one_project

            # check init entity was called
            mock_init_entity.assert_called_with('project', projects_with_name[0]['id'])


def test_init_asset(asset_init_args, asset_init_args_no_asset_type, ktrack_instance, ktrack_registered_project):
    # mock get_ktrack
    project, project_context_path = ktrack_registered_project

    with mock.patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        with mock.patch('kttk.init_entity') as mock_init_entity:
            with mock.patch('os.getcwd') as mock_get_cwd:
                mock_get_cwd.return_value = project_context_path

                mock_get_ktrack.return_value = ktrack_instance

                # should fail when no asset type is provided

                with pytest.raises(NoAssetType):
                    execute_cmd(asset_init_args_no_asset_type)

                execute_cmd(asset_init_args)

                # check project exists in DB
                assets_with_name = ktrack_instance.find('asset', [['code', 'is', ASSET_NAME]])
                only_one_project = len(assets_with_name) == 1

                assert only_one_project

                # check init entity was called
                mock_init_entity.assert_called_with('asset', assets_with_name[0]['id'])

def test_init_asset_no_context_registered(asset_init_args, ktrack_instance):

    with mock.patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        with mock.patch('kttk.init_entity') as mock_init_entity:
            with mock.patch('os.getcwd') as mock_get_cwd:
                mock_get_cwd = '/mnt/'+str(uuid.uuid4())

                with pytest.raises(PathNotRegistered):
                    execute_cmd(asset_init_args)
