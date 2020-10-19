from typing import List, IO

from kttk.commands.command_registry import CommandRegistry


class CommandRunner(object):
    def __init__(self, stream, command_registry):
        # type: (IO, CommandRegistry) -> None
        self._stream = stream
        self._command_registry = command_registry

    def run(self, args):
        # type: (List[str]) -> None
        command_name = args[0]

        commands = self._command_registry.get_available_commands()
        command = commands.get(command_name)

        if not command:
            self._stream.write("Unknown command: {}".format(command_name))
            return

        command(self._stream).run(args[1:])
