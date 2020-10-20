from typing import List, IO

from kttk.commands.abstract_command import AbstractCommand
from kttk.commands.dcc.create_new_command import DccCreateNewCommand


class DccCommand(AbstractCommand):
    def __init__(self, stream, create_command):
        # type: (IO, DccCreateNewCommand) -> None
        super(DccCommand, self).__init__(stream)
        self._create_command = create_command

    def run(self, args):
        # type: (List[str]) -> None
        command_name = args[0]
        if command_name == "create":
            self._create_command.run(args[1:])
        else:
            self._stream.write("Unknown command: {}".format(command_name))
