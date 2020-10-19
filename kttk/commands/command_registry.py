from typing import Dict, Callable

import kttk
from ktrack_api.mongo_impl.mongo_repositories import (
    MongoProjectRepository,
    MongoAssetRepository,
)
from kttk.commands.abstract_command import AbstractCommand
from kttk.commands.basic.create_asset_command import CreateAssetCommand
from kttk.commands.basic.create_project_command import CreateProjectCommand


class CommandRegistry(object):
    def get_available_commands(self):
        # type: () -> Dict[str, Callable[[any], AbstractCommand]]
        return {
            "create-project": self._create_project_command,
            "create-asset": self._create_asset_command,
        }

    def _create_project_command(self, stream):
        return CreateProjectCommand(stream, MongoProjectRepository(), kttk.init_entity)

    def _create_asset_command(self, stream):
        return CreateAssetCommand(
            stream, MongoProjectRepository(), MongoAssetRepository(), kttk.init_entity
        )
