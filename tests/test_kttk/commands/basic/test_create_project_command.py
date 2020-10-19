from mock import MagicMock

from kttk.commands.basic.create_project_command import CreateProjectCommand
from kttk.domain.entities import Project


def test_should_create_project():
    stream = MagicMock()
    project_repository = MagicMock()
    entity_initializer = MagicMock()
    create_project_command = CreateProjectCommand(
        stream, project_repository, entity_initializer
    )

    create_project_command.run(["test_project_name"])

    project_repository.save.assert_called_with(Project(name="test_project_name"))


def test_should_not_exit():
    stream = MagicMock()
    ktrack_api = MagicMock()
    entity_initializer = MagicMock()
    create_project_command = CreateProjectCommand(
        stream, ktrack_api, entity_initializer
    )

    create_project_command.run([])
