import datetime
import os
import subprocess

import mock
import pytest
from mock import MagicMock

import ktrack_api
from kttk import path_cache_manager
from kttk.context import Context
from scripts import ktrack_command
from tests import integration_test_only

FINDING_DORY_PATH = "M:/Projekte/{}/Finding_Dory".format(datetime.datetime.now().year)


@pytest.fixture
def console_bot():
    class ConsoleBot(object):
        def run(self, command, cwd=os.getcwd()):
            self.p = subprocess.Popen(command, stdout=subprocess.PIPE, cwd=cwd)
            self.result = self.p.communicate()[0]

    return ConsoleBot()


@pytest.fixture
def mock_print_result():
    # type: () -> MagicMock
    with mock.patch("scripts.ktrack_command.print_result") as mock_print_result:
        yield mock_print_result


@pytest.fixture
def cwd_shot010():
    # type: () -> MagicMock
    with mock.patch("os.getcwd") as mock_get_cwd:
        mock_get_cwd.return_value = os.path.join(FINDING_DORY_PATH, "Shots", "shot010")
        yield mock_get_cwd


@pytest.fixture
def cwd_hank():
    # type: () -> MagicMock
    with mock.patch("os.getcwd") as mock_get_cwd:
        mock_get_cwd.return_value = os.path.join(
            FINDING_DORY_PATH, "Assets", "character", "Hank"
        )
        yield mock_get_cwd


@pytest.fixture
def cwd_finding_dory():
    # type: () -> MagicMock
    with mock.patch("os.getcwd") as mock_get_cwd:
        mock_get_cwd.return_value = FINDING_DORY_PATH
        yield mock_get_cwd


@pytest.fixture
def cwd_no_context():
    # type: () -> MagicMock
    with mock.patch("os.getcwd") as mock_get_cwd:
        mock_get_cwd.return_value = "some_path"
        yield mock_get_cwd


#####  some helpers for validation
def project_has_asset_with_code(project_id, asset_code):
    kt = ktrack_api.get_ktrack()

    assets = kt.find(
        "asset", [["project", "is", {"type": "project", "id": project_id}]]
    )

    for asset in assets:
        if asset["code"] == asset_code:
            return True

    return False


def project_has_shot_with_code(project_id, shot_code):
    kt = ktrack_api.get_ktrack()

    assets = kt.find("shot", [["project", "is", {"type": "project", "id": project_id}]])

    for asset in assets:
        if asset["code"] == shot_code:
            return True

    return False


def project_has_task_with_name(project_id, task_name):
    kt = ktrack_api.get_ktrack()

    tasks = kt.find("task", [["project", "is", {"type": "project", "id": project_id}]])

    for task in tasks:
        if task["name"] == task_name:
            return True

    return False


## tests


def test_name_or_code():
    # test name
    assert ktrack_command.get_name_or_code({"name": "my_name"}) == "my_name"

    # test code
    assert ktrack_command.get_name_or_code({"code": "my_name"}) == "my_name"

    assert ktrack_command.get_name_or_code({"namee": "my_name"}) is None


def test_print_context_invalid_path(mock_print_result):
    # test the context method of ktrack command

    # test not registered path

    ktrack_command.print_context("some_path")
    mock_print_result.assert_called_once_with(
        "No Context registered for path some_path"
    )


def test_print_context_valid_path(mock_print_result):
    # test registered path
    with mock.patch("kttk.path_cache_manager.context_from_path") as mock_from_path:
        mock_from_path.return_value = Context()
        ktrack_command.print_context("some_path")
        mock_print_result.assert_called_once_with(mock_from_path.return_value)


@integration_test_only
class TestContextCommand(object):
    @staticmethod
    def test_valid_path(bootstrapped_project, mock_print_result):
        ktrack_command.print_context(FINDING_DORY_PATH)

        mock_print_result.assert_called_with(Context(project=bootstrapped_project))

    @staticmethod
    def test_invalid_path(mock_print_result):
        ktrack_command.print_context("some_path")
        mock_print_result.assert_called_with(
            "No Context registered for path {}".format("some_path")
        )


@integration_test_only
class TestCreateCommand(object):
    @staticmethod
    def test_create_project():
        # dont need to mock os.getcwd, doesnt matter for project

        # todo we need something to unregister paths / entities
        pass

    @staticmethod
    def test_create_no_context(mock_print_result, cwd_no_context):
        # test what happens if we run create without being in a directory for a context
        ktrack_command.create("shot", "shot010")

        mock_print_result.assert_called_with("No context provided for path")

    @staticmethod
    def test_create_asset_no_asset_type(
        bootstrapped_project, mock_print_result, cwd_finding_dory
    ):
        ktrack_command.create("asset", "Nemo")

        mock_print_result.assert_called_with("no asset type")

    @staticmethod
    def test_create_asset(bootstrapped_project, cwd_finding_dory):
        asset_name = "Nemo"
        # ACT and create the asset
        ktrack_command.create("asset", asset_name, asset_type="character")

        # now check everything is correct

        # check asset was created in database
        assert project_has_asset_with_code(bootstrapped_project["id"], asset_name)

        # check asset folder exists on disk
        asset_folder = os.path.join(FINDING_DORY_PATH, "Assets", "character", "Nemo")
        assert os.path.exists(asset_folder)

        # make sure we can get context from this path correctly
        context = path_cache_manager.context_from_path(asset_folder)
        assert context

        # make sure context project is correct
        assert context.project["id"] == bootstrapped_project["id"]
        assert context.entity

        # make sure context entity is correct
        kt = ktrack_api.get_ktrack()
        assert kt.find_one("asset", context.entity["id"])["code"] == "Nemo"

    @staticmethod
    def test_create_shot(bootstrapped_project, cwd_finding_dory):
        shot_code = "shot050"
        # ACT and create the asset
        ktrack_command.create("shot", shot_code)

        # now check everything is correct

        # check asset was created in database
        assert project_has_shot_with_code(bootstrapped_project["id"], shot_code)

        # check asset folder exists on disk
        shots_folder = os.path.join(FINDING_DORY_PATH, "Shots", shot_code)
        assert os.path.exists(shots_folder)

        # make sure we can get context from this path correctly
        context = path_cache_manager.context_from_path(shots_folder)
        assert context

        # make sure context project is correct
        assert context.project["id"] == bootstrapped_project["id"]
        assert context.entity

        # make sure context entity is correct
        kt = ktrack_api.get_ktrack()
        assert kt.find_one("shot", context.entity["id"])["code"] == "shot050"

    @staticmethod
    def test_create_task_no_step(
        bootstrapped_project, mock_print_result, cwd_finding_dory
    ):
        # create task without step for asset Hank
        ktrack_command.create("task", "some_step")

        # make sure 'no task step' was printed to console
        mock_print_result.assert_called_with("no task step")

    @staticmethod
    def test_create_task_no_asset_shot(
        bootstrapped_project, mock_print_result, cwd_finding_dory
    ):
        # try to create a task for a context with no entity
        ktrack_command.create("task", "some_step", task_step="prep")

        # make sure error was printed
        mock_print_result.assert_called_with("No entity provided for task")

    @staticmethod
    def test_create_task_asset(bootstrapped_project, mock_print_result, cwd_hank):
        # create a texturing task for asset Hank
        task_name = "texturing_hank"
        ktrack_command.create("task", task_name, task_step="prep")

        # make sure a task with the name exists for the project
        assert project_has_task_with_name(bootstrapped_project["id"], task_name)

        # todo make sure current user is assigned

    @staticmethod
    def test_create_task_shot(bootstrapped_project, cwd_shot010):
        # create a prep task for shot shot010
        task_name = "preping_the_test"
        ktrack_command.create("task", task_name, task_step="prep")

        # make sure a task with the name exists for the project
        assert project_has_task_with_name(bootstrapped_project["id"], task_name)

        # todo make sure current user is assigned


@integration_test_only
class TestFindOneCommand(object):
    @staticmethod
    def test_find_non_existing_id(mock_print_result):
        ktrack_command.find_one("project", "5b6ef17e6e87ff1c2064aa24")

        mock_print_result.assert_called_with(
            'Entity of type "{}" and id "{}" not found..'.format(
                "project", "5b6ef17e6e87ff1c2064aa24"
            )
        )

    @staticmethod
    def test_find_existing(bootstrapped_project):
        with mock.patch("pprint.PrettyPrinter.pprint") as mock_pprint:
            ktrack_command.find_one("project", bootstrapped_project["id"])

            mock_pprint.assert_called_once()

    @staticmethod
    def test_find_non_existing_entity_type(mock_print_result):
        entity_type = "after_eight"
        ktrack_command.find_one(entity_type, "5b6ef17e6e87ff1c2064aa24")

        mock_print_result.assert_called_with(
            "Entity type '{}' does not exist".format(entity_type)
        )


@integration_test_only
class TestShowCommand(object):
    @staticmethod
    def test_missing_entity_type(mock_print_result):
        # apply show command
        ktrack_command.show("peter")

        # validate
        mock_print_result.assert_called_with("Entity type peter does not exist")

    @staticmethod
    def test_no_entities_found(mock_print_result):
        with mock.patch("ktrack_api.ktrack.Ktrack.find") as mock_find:
            mock_find.return_value = None

            ktrack_command.show("project")

            mock_print_result.assert_called_with("No entities of type project found..")

    def test_entities_found(self, bootstrapped_project):
        ktrack_command.show("project")


@integration_test_only
class TestTaskPresetCommand(object):
    @staticmethod
    def test_task_preset_shot(bootstrapped_project, mock_print_result, cwd_shot010):
        # old task count
        kt = ktrack_api.get_ktrack()
        old_task_count = len(kt.find("task", [["project", "is", bootstrapped_project]]))

        # apply task preset
        ktrack_command.task_preset()

        # validate
        new_task_count = len(kt.find("task", [["project", "is", bootstrapped_project]]))
        assert new_task_count == (old_task_count + 3)

    @staticmethod
    def test_task_preset_asset(bootstrapped_project, mock_print_result, cwd_hank):
        # old task count
        kt = ktrack_api.get_ktrack()
        old_task_count = len(kt.find("task", [["project", "is", bootstrapped_project]]))

        # apply task preset
        ktrack_command.task_preset()

        # validate
        new_task_count = len(kt.find("task", [["project", "is", bootstrapped_project]]))
        assert new_task_count == (old_task_count + 2)

    @staticmethod
    def test_invalid_path(mock_print_result, cwd_no_context):
        # try to apply task preset for invalid folder with no contexst
        ktrack_command.task_preset()

        # make sure error message was printed
        mock_print_result.assert_called_with(
            "No Context registered for path {}".format("some_path")
        )
