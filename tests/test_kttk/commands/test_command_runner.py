from mock import MagicMock

from kttk.commands.command_runner import CommandRunner


def test_should_create_command_and_run():
    stream = MagicMock()
    command_registry = MagicMock()
    command = MagicMock()
    command_registry.get_available_commands.return_value = {
        'test': lambda x: command
    }
    command_runner = CommandRunner(stream, command_registry)

    command_runner.run(['test', 'my_arg'])

    command.run.assert_called_with(['my_arg'])


def test_should_write_unknown_command():
    stream = MagicMock()
    command_registry = MagicMock()
    command_registry.get_available_commands.return_value = {
    }
    command_runner = CommandRunner(stream, command_registry)

    command_runner.run(['test', 'my_arg'])

    stream.write.assert_called_with("Unknown command: test")
