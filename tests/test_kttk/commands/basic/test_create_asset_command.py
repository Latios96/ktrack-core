from mock import MagicMock

from kttk.commands.basic.create_asset_command import (
    _format_asset_type,
    CreateAssetCommand,
)
from kttk.domain.entities import Asset, Project


def test_format_asset_type():
    assert _format_asset_type("pRop") == "Prop"


def test_should_create_project():
    stream = MagicMock()
    project_repository = MagicMock()
    asset_repository = MagicMock()
    entity_initializer = MagicMock()
    create_project_command = CreateAssetCommand(
        stream, project_repository, asset_repository, entity_initializer
    )
    project_repository.find_by_name.return_value = Project(id="123", name="test")

    create_project_command.run(["test:test_asset", "pRop"])

    asset_repository.save.assert_called_with(
        Asset(name="test_asset", asset_type="Prop", project="123")
    )


def test_should_error_project_not_found():
    stream = MagicMock()
    project_repository = MagicMock()
    asset_repository = MagicMock()
    entity_initializer = MagicMock()
    create_project_command = CreateAssetCommand(
        stream, project_repository, asset_repository, entity_initializer
    )
    project_repository.find_by_name.return_value = None

    create_project_command.run(["test:test_asset", "pRop"])

    stream.write.asset_called_with('Could not find project with name "test"')


def test_should_not_exit():
    stream = MagicMock()
    project_repository = MagicMock()
    asset_repository = MagicMock()
    entity_initializer = MagicMock()
    create_project_command = CreateAssetCommand(
        stream, project_repository, asset_repository, entity_initializer
    )

    create_project_command.run([])
