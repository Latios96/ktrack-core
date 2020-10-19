from mock import MagicMock

from kttk.commands.basic.create_project_command import CreateProjectCommand


def test_should_create_project():
    stream = MagicMock()
    ktrack_api = MagicMock()
    entity_initializer = MagicMock()
    create_project_command = CreateProjectCommand(stream, ktrack_api, entity_initializer)

    create_project_command.run(['test_project_name'])

    ktrack_api.create.assert_called_with('project', {'name': 'test_project_name'})


def test_should_not_exit():
    stream = MagicMock()
    ktrack_api = MagicMock()
    entity_initializer = MagicMock()
    create_project_command = CreateProjectCommand(stream, ktrack_api, entity_initializer)

    create_project_command.run([])
