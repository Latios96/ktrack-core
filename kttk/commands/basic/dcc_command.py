import argparse

from typing import List, IO, Callable

import kttk
from ktrack_api.repositories import ProjectRepository, AssetRepository
from kttk import logger
from kttk.commands.abstract_command import AbstractCommand
from kttk.commands.basic.create_new_command import DccCreateNewCommand
from kttk.context import Context
from kttk.domain.entities import Asset, KtrackId
from kttk.domain.entity_reference import EntityReference
from kttk.file_manager.file_manager import FileManager
from kttk.references.serialized_task_reference_parser import (
    SerializedTaskReferenceParser,
)
from kttk.references.serialized_workfile_reference_parser import (
    SerializedWorkfileReferenceParser,
)
from kttk.references.task_reference_resolver import TaskReferenceResolver
from kttk.references.workfile_reference_resolver import WorkfileReferenceResolver
from kttk.task_preset_applicator import TaskPresetApplicator


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
