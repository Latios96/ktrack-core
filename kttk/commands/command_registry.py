from typing import Dict, Callable

import kttk
from ktrack_api.mongo_impl.mongo_repositories import (
    MongoProjectRepository,
    MongoAssetRepository,
    MongoTaskRepository,
    MongoShotRepository,
)
from kttk import engines
from kttk.commands.abstract_command import AbstractCommand
from kttk.commands.basic.create_asset_command import CreateAssetCommand
from kttk.commands.basic.create_new_command import DccCreateNewCommand
from kttk.commands.basic.create_project_command import CreateProjectCommand
from kttk.commands.basic.dcc_command import DccCommand
from kttk.file_manager.file_manager import FileManager
from kttk.references.serialized_task_reference_parser import (
    SerializedTaskReferenceParser,
)
from kttk.references.task_reference_resolver import TaskReferenceResolver
from kttk.task_preset_applicator import TaskPresetApplicator
from kttk_widgets.view_callback_mixin.view_callback_qt_impl import (
    ViewCallbackQtImplementation,
)


class CommandRegistry(object):
    def get_available_commands(self):
        # type: () -> Dict[str, Callable[[any], AbstractCommand]]
        commands = {
            "create-project": self._create_project_command,
            "create-asset": self._create_asset_command,
        }

        self._add_dcc_commands_if_possible(commands)

        return commands

    def _add_dcc_commands_if_possible(self, commands):
        if engines.current_engine():
            commands["dcc"] = self._create_dcc_command

    def _create_project_command(self, stream):
        return CreateProjectCommand(stream, MongoProjectRepository(), kttk.init_entity)

    def _create_asset_command(self, stream):
        return CreateAssetCommand(
            stream,
            MongoProjectRepository(),
            MongoAssetRepository(),
            kttk.init_entity,
            TaskPresetApplicator(MongoTaskRepository(), kttk.init_entity),
        )

    def _create_dcc_command(self, stream):
        view_callback_mixin = ViewCallbackQtImplementation()
        file_manager = FileManager(view_callback_mixin)
        create_new_command = DccCreateNewCommand(
            stream,
            file_manager,
            SerializedTaskReferenceParser(),
            TaskReferenceResolver(
                MongoProjectRepository(),
                MongoAssetRepository(),
                MongoShotRepository(),
                MongoTaskRepository(),
            ),
        )
        return DccCommand(stream, create_new_command)
