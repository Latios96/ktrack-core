import argparse

from typing import List, IO, Callable

from ktrack_api.repositories import ProjectRepository
from kttk import logger
from kttk.commands.abstract_command import AbstractCommand
from kttk.domain.entities import Project, KtrackId


class CreateProjectCommand(AbstractCommand):
    def __init__(self, stream, project_repository, entity_initializer):
        # type: (IO, ProjectRepository, Callable[[str, KtrackId], None]) -> None
        super(CreateProjectCommand, self).__init__(stream)
        self._project_repository = project_repository
        self._entity_initializer = entity_initializer

    def run(self, args):
        # type: (List[str]) -> None
        parser = argparse.ArgumentParser(description="Create a new project")
        parser.add_argument("name", help="the project name")

        try:
            args = parser.parse_args(args)
        except SystemExit as e:
            return

        self._create_project(args)

    def _create_project(self, args):
        project_name = args.name
        logger.info("initialise project")
        logger.info("create project in database..")
        project = self._project_repository.save(
            Project(name=project_name)
        )  # type: Project
        logger.info("Created project {} with id {}".format(project.name, project.id))
        logger.info("initialise project on disk..")
        self._entity_initializer("project", project.id)
        logger.info(
            "{entity_type} with id {entity_id} initialised. Done.".format(
                entity_type="project", entity_id=project.id
            )
        )
