import pytest
from mock import MagicMock

from kttk.domain.entities import Project, Asset, Task
from kttk.references.entity_types import ReferenceEntityType
from kttk.references.task_reference import SerializedTaskReference, TaskReference
from kttk.references.task_reference_resolver import TaskReferenceResolver


def test_should_resolve_reference_correctly():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    workfile_reference_resolver = TaskReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
    )
    serialized_reference = SerializedTaskReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
    )
    project = Project(name="SnowGlobe")
    entity = Asset(name="Rheinturm")
    task = Task(name="modelling")
    mock_project_repository.find_by_name.return_value = project
    mock_asset_repository.find_by_project_and_name.return_value = entity
    mock_task_repository.find_by_project_and_name.return_value = task

    workfile_reference = workfile_reference_resolver.resolve(serialized_reference)

    assert workfile_reference == TaskReference(
        project=project,
        entity_type=ReferenceEntityType.ASSET,
        entity=entity,
        task=task,
    )


def test_should_not_resolve_reference_missing_project():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    workfile_reference_resolver = TaskReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
    )
    serialized_reference = SerializedTaskReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
    )
    mock_project_repository.find_by_name.return_value = None

    with pytest.raises(ValueError):
        workfile_reference_resolver.resolve(serialized_reference)


def test_should_not_resolve_reference_missing_shot():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    workfile_reference_resolver = TaskReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
    )
    serialized_reference = SerializedTaskReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.SHOT,
        entity_name="Rheinturm",
        task_name="modelling",
    )
    project = Project(name="SnowGlobe")
    mock_project_repository.find_by_name.return_value = project
    mock_shot_repository.find_by_project_and_name.return_value = None

    with pytest.raises(ValueError):
        workfile_reference_resolver.resolve(serialized_reference)


def test_should_not_resolve_reference_missing_asset():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    workfile_reference_resolver = TaskReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
    )
    serialized_reference = SerializedTaskReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
    )
    project = Project(name="SnowGlobe")
    mock_project_repository.find_by_name.return_value = project
    mock_asset_repository.find_by_project_and_name.return_value = None

    with pytest.raises(ValueError):
        workfile_reference_resolver.resolve(serialized_reference)


def test_should_not_resolve_reference_missing_task():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    workfile_reference_resolver = TaskReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
    )
    serialized_reference = SerializedTaskReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
    )
    project = Project(name="SnowGlobe")
    entity = Asset(name="Rheinturm")
    mock_project_repository.find_by_name.return_value = project
    mock_asset_repository.find_by_project_and_name.return_value = entity
    mock_task_repository.find_by_project_and_name.return_value = None

    with pytest.raises(ValueError):
        workfile_reference_resolver.resolve(serialized_reference)
