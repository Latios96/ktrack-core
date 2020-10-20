import pytest
from mock import MagicMock

from kttk.domain.entities import Project, Asset, Task, Workfile
from kttk.references.entity_types import ReferenceEntityType
from kttk.references.workfile_reference import (
    SerializedWorkfileReference,
    WorkfileReference,
)
from kttk.references.workfile_reference_resolver import WorkfileReferenceResolver


def test_should_resolve_reference_correctly_with_latest():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    mock_workfile_repository = MagicMock()
    workfile_reference_resolver = WorkfileReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
        mock_workfile_repository,
    )
    serialized_reference = SerializedWorkfileReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
        version_identifier="latest",
    )
    project = Project(name="SnowGlobe")
    entity = Asset(name="Rheinturm")
    task = Task(name="modelling")
    workfile = Workfile()
    mock_project_repository.find_by_name.return_value = project
    mock_asset_repository.find_by_project_and_name.return_value = entity
    mock_task_repository.find_by_project_and_name.return_value = task
    mock_workfile_repository.find_by_task_latest.return_value = workfile

    workfile_reference = workfile_reference_resolver.resolve(serialized_reference)

    assert workfile_reference == WorkfileReference(
        project=project,
        entity_type=ReferenceEntityType.ASSET,
        entity=entity,
        task=task,
        workfile=workfile,
    )


def test_should_resolve_reference_correctly_with_version():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    mock_workfile_repository = MagicMock()
    workfile_reference_resolver = WorkfileReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
        mock_workfile_repository,
    )
    serialized_reference = SerializedWorkfileReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
        version_identifier="v009",
    )
    project = Project(name="SnowGlobe")
    entity = Asset(name="Rheinturm")
    task = Task(name="modelling")
    workfile = Workfile()
    mock_project_repository.find_by_name.return_value = project
    mock_asset_repository.find_by_project_and_name.return_value = entity
    mock_task_repository.find_by_project_and_name.return_value = task
    mock_workfile_repository.find_by_task_and_version_number.return_value = workfile

    workfile_reference = workfile_reference_resolver.resolve(serialized_reference)

    assert workfile_reference == WorkfileReference(
        project=project,
        entity_type=ReferenceEntityType.ASSET,
        entity=entity,
        task=task,
        workfile=workfile,
    )


def test_should_not_resolve_reference_missing_project():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    mock_workfile_repository = MagicMock()
    workfile_reference_resolver = WorkfileReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
        mock_workfile_repository,
    )
    serialized_reference = SerializedWorkfileReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
        version_identifier="latest",
    )
    mock_project_repository.find_by_name.return_value = None

    with pytest.raises(ValueError):
        workfile_reference_resolver.resolve(serialized_reference)


def test_should_not_resolve_reference_missing_shot():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    mock_workfile_repository = MagicMock()
    workfile_reference_resolver = WorkfileReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
        mock_workfile_repository,
    )
    serialized_reference = SerializedWorkfileReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.SHOT,
        entity_name="Rheinturm",
        task_name="modelling",
        version_identifier="latest",
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
    mock_workfile_repository = MagicMock()
    workfile_reference_resolver = WorkfileReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
        mock_workfile_repository,
    )
    serialized_reference = SerializedWorkfileReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
        version_identifier="latest",
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
    mock_workfile_repository = MagicMock()
    workfile_reference_resolver = WorkfileReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
        mock_workfile_repository,
    )
    serialized_reference = SerializedWorkfileReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
        version_identifier="latest",
    )
    project = Project(name="SnowGlobe")
    entity = Asset(name="Rheinturm")
    mock_project_repository.find_by_name.return_value = project
    mock_asset_repository.find_by_project_and_name.return_value = entity
    mock_task_repository.find_by_project_and_name.return_value = None

    with pytest.raises(ValueError):
        workfile_reference_resolver.resolve(serialized_reference)


def test_should_not_resolve_reference_correctly_missing_workfile():
    mock_project_repository = MagicMock()
    mock_asset_repository = MagicMock()
    mock_shot_repository = MagicMock()
    mock_task_repository = MagicMock()
    mock_workfile_repository = MagicMock()
    workfile_reference_resolver = WorkfileReferenceResolver(
        mock_project_repository,
        mock_asset_repository,
        mock_shot_repository,
        mock_task_repository,
        mock_workfile_repository,
    )
    serialized_reference = SerializedWorkfileReference(
        project_name="SnowGlobe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="Rheinturm",
        task_name="modelling",
        version_identifier="latest",
    )
    project = Project(name="SnowGlobe")
    entity = Asset(name="Rheinturm")
    task = Task(name="modelling")
    mock_project_repository.find_by_name.return_value = project
    mock_asset_repository.find_by_project_and_name.return_value = entity
    mock_task_repository.find_by_project_and_name.return_value = task
    mock_workfile_repository.find_by_task_latest.return_value = None

    with pytest.raises(ValueError):
        workfile_reference_resolver.resolve(serialized_reference)
