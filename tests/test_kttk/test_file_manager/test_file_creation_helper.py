import os

import pytest
from mock import MagicMock, patch

from kttk.context import Context
from kttk.file_manager.file_creation_helper import FileCreationHelper


@pytest.fixture
def mock_engine():
    # mock engine
    engine_mock = MagicMock()
    engine_mock.file_extension = ".mb"
    engine_mock.name = "Maya"
    return engine_mock


@pytest.fixture()
def file_creation_helper(mock_engine):
    return FileCreationHelper(mock_engine)


def test_context_is_valid(file_creation_helper, project_dict, shot_dict, task_dict):
    # valid context
    context = Context(
        project=project_dict, entity=shot_dict, task=task_dict, step="anim"
    )

    assert file_creation_helper._context_is_valid_for_file_creation(context)

    # invalid contexts
    with pytest.raises(ValueError):
        context = Context(project=project_dict, entity=shot_dict, task=task_dict)
        assert (
            file_creation_helper._context_is_valid_for_file_creation(context) == False
        )

    with pytest.raises(ValueError):
        context = Context(project=project_dict, entity=shot_dict)
        assert (
            file_creation_helper._context_is_valid_for_file_creation(context) == False
        )

    with pytest.raises(ValueError):
        context = Context(project=project_dict)
        assert (
            file_creation_helper._context_is_valid_for_file_creation(context) == False
        )

    with pytest.raises(ValueError):
        context = Context()
        assert (
            file_creation_helper._context_is_valid_for_file_creation(context) == False
        )


def test_get_template_file(file_creation_helper):
    # mock engine
    engine_mock = MagicMock()
    engine_mock.file_extension = ".mb"
    file_creation_helper._engine = engine_mock

    template_file_path = file_creation_helper._get_template_file_path()
    assert "templates/template.mb" in template_file_path


def test_create_new_workfile(file_creation_helper):
    # mock create from exisitng
    mock_create_from_existing = MagicMock()

    file_creation_helper._create_workfile_from = mock_create_from_existing

    file_creation_helper._create_new_workfile(Context())

    assert file_creation_helper._create_workfile_from.called


def test_create_workfile_from_non_existing(
    file_creation_helper, populated_context, ktrack_instance
):
    # mock database
    with patch("ktrack_api.get_ktrack") as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance

        new_workfile = file_creation_helper._create_workfile_from(
            populated_context, {"version_number": 0}
        )

        assert new_workfile["version_number"] == 1
        assert new_workfile["name"] == "my_entity_task_anim_v001.mb"
        assert os.path.normpath(new_workfile["path"]) == os.path.normpath(
            "M:/Projekte/2019/my_project/Assets/prop/my_entity/my_entity_Maya/my_entity_task_anim_v001.mb"
        )
        assert new_workfile["created_from"] is None


def test_create_workfile_from_existing(
    file_creation_helper, populated_context, ktrack_instance
):
    # mock database
    with patch("ktrack_api.get_ktrack") as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance

        previos_workfile = {"version_number": 0, "id": "some_id"}
        new_workfile = file_creation_helper._create_workfile_from(
            populated_context, previos_workfile
        )

        assert new_workfile["created_from"] == previos_workfile


def test_create_workfile_from_existing_with_comment(
    file_creation_helper, populated_context, ktrack_instance
):
    # mock database
    with patch("ktrack_api.get_ktrack") as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance

        previos_workfile = {"version_number": 0, "id": "some_id"}
        new_workfile = file_creation_helper._create_workfile_from(
            populated_context, previos_workfile, comment="MY COMMENT"
        )

        assert new_workfile["created_from"] == previos_workfile
        assert new_workfile["comment"] == "MY COMMENT"


def test_get_highest_workfile_existing_workfiles(file_creation_helper, ktrack_instance):
    # mock database
    with patch("ktrack_api.get_ktrack") as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance

        # create task and some workfiles
        task = ktrack_instance.create(
            "task",
            {
                "project": {"type": "project", "id": "some_id"},
                "entity": {"code": "some_entity"},
            },
        )

        for i in range(5):
            ktrack_instance.create(
                "workfile",
                {
                    "entity": task,
                    "version_number": i,
                    "path": "some_path",
                    "project": {"type": "project", "id": "some_id"},
                },
            )

        highest_workfile = file_creation_helper._get_highest_workfile(
            Context(task=task)
        )

        assert highest_workfile["version_number"] == 4


def test_get_highest_workfile_no_workfiles(file_creation_helper, ktrack_instance):
    # mock database
    with patch("ktrack_api.get_ktrack") as mock_get_ktrack:
        mock_get_ktrack.return_value = ktrack_instance

        # create task and some workfiles
        task = ktrack_instance.create(
            "task",
            {
                "project": {"type": "project", "id": "some_id"},
                "entity": {"code": "some_entity"},
            },
        )

        highest_workfile = file_creation_helper._get_highest_workfile(
            Context(task=task)
        )

        assert highest_workfile is None
