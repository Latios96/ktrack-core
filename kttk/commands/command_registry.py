from typing import List

from kttk.commands.abstract_command import AbstractCommand


class CommandRegistry(object):

    def get_available_commands(self):
        # type: () -> List[AbstractCommand]
        raise NotImplementedError()
