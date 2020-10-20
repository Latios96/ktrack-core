import argparse

from typing import List, IO, Callable

import kttk
from ktrack_api.repositories import ProjectRepository, AssetRepository
from kttk import logger
from kttk.commands.abstract_command import AbstractCommand
from kttk.context import Context
from kttk.domain.entities import Asset, KtrackId
from kttk.domain.entity_reference import EntityReference
from kttk.file_manager.file_manager import FileManager
from kttk.references.entity_types import ReferenceEntityType
from kttk.references.serialized_task_reference_parser import (
    SerializedTaskReferenceParser,
)
from kttk.references.serialized_workfile_reference_parser import (
    SerializedWorkfileReferenceParser,
)
from kttk.references.task_reference_resolver import TaskReferenceResolver
from kttk.references.workfile_reference_resolver import WorkfileReferenceResolver
from kttk.task_preset_applicator import TaskPresetApplicator


class DccCreateNewCommand(AbstractCommand):
    def __init__(
        self,
        stream,
        file_manager,
        serialized_task_reference_parser,
        serialized_task_reference_resolver,
    ):
        # type: (IO, FileManager, SerializedTaskReferenceParser, TaskReferenceResolver) -> None
        super(DccCreateNewCommand, self).__init__(stream)
        self._serialized_task_reference_resolver = serialized_task_reference_resolver
        self._serialized_task_reference_parser = serialized_task_reference_parser
        self._file_manager = file_manager

    def run(self, args):
        # type: (List[str]) -> None
        parser = argparse.ArgumentParser(description="Create a new asset")
        parser.add_argument(
            "workfile_reference",
            help="the workfile reference (project_name:entity_type:entity_name:task_name:version_identifier)",
        )

        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return

        serialized_reference = self._serialized_task_reference_parser.parse(
            parsed_args.workfile_reference
        )
        task_reference = self._serialized_task_reference_resolver.resolve(
            serialized_reference
        )
        print("Task Reference: {}".format(task_reference))

        self._file_manager.create(
            Context(
                project={"type": "project", "id": task_reference.project.id},
                entity={
                    "type": "asset"
                    if task_reference.entity_type == ReferenceEntityType.ASSET
                    else "shot",
                    "id": task_reference.entity.id,
                },
                step=task_reference.task.step,
                task={"type": "task", "id": task_reference.task.id},
                workfile=None,
                user=kttk.restore_user(),
            )
        )  # todo better user handling
