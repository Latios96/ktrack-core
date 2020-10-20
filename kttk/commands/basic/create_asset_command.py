import argparse

from typing import List, IO, Callable

from ktrack_api.repositories import ProjectRepository, AssetRepository
from kttk import logger
from kttk.commands.abstract_command import AbstractCommand
from kttk.domain.entities import Asset, KtrackId
from kttk.domain.entity_reference import EntityReference
from kttk.task_preset_applicator import TaskPresetApplicator


class CreateAssetCommand(AbstractCommand):
    def __init__(
        self,
        stream,
        project_repository,
        asset_repository,
        entity_initializer,
        task_preset_applicator,
    ):
        # type: (IO, ProjectRepository, AssetRepository, Callable[[str, KtrackId], None], TaskPresetApplicator) -> None
        super(CreateAssetCommand, self).__init__(stream)
        self._project_repository = project_repository
        self._asset_repository = asset_repository
        self._entity_initializer = entity_initializer
        self._task_preset_applicator = task_preset_applicator

    def run(self, args):
        # type: (List[str]) -> None
        parser = argparse.ArgumentParser(description="Create a new asset")
        parser.add_argument(
            "entity_reference", help="the asset reference (project_name:asset_name)"
        )
        parser.add_argument("asset_type", help="the asset type")

        try:
            parsed_args = parser.parse_args(args)
        except SystemExit as e:
            return

        entity_reference = EntityReference.parse(parsed_args.entity_reference)
        project = self._project_repository.find_by_name(entity_reference.project_name)
        if not project:
            self._stream.write(
                'Could not find project with name "{}"'.format(
                    entity_reference.project_name
                )
            )
            return

        self._create_asset(entity_reference, parsed_args, project)

    def _create_asset(self, entity_reference, parsed_args, project):
        logger.info("Initialise Asset")
        logger.info("Create Asset in database..")

        asset = Asset(
            project=project.id,
            name=entity_reference.entity_name,
            asset_type=_format_asset_type(parsed_args.asset_type),
        )
        asset = self._asset_repository.save(asset)

        logger.info("Created Asset {} with id {}.".format(asset.name, asset.asset_type))

        logger.info("Initialise entity on disk..")
        self._entity_initializer("asset", asset.id)
        logger.info("Asset with id {} initialised.".format(asset.id))

        logger.info("Creating tasks for Asset {}...".format(asset.name))
        self._task_preset_applicator.apply("asset", project.id, asset.id)
        logger.info("Tasks created for Asset {}".format(asset.name))
        logger.info("Done.")


def _format_asset_type(asset_type):
    # type: (str) -> str
    asset_type = asset_type.lower()

    return asset_type[0].upper() + asset_type[1:]
