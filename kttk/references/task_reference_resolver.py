from ktrack_api.repositories import (
    ProjectRepository,
    AssetRepository,
    ShotRepository,
    TaskRepository,
)
from kttk.domain.entities import VersionNumber
from kttk.references.entity_types import ReferenceEntityType
from kttk.references.task_reference import SerializedTaskReference, TaskReference
from kttk.references.workfile_reference import (
    WorkfileReference,
)


class TaskReferenceResolver(object):
    def __init__(
        self,
        project_repository,
        asset_repository,
        shot_repository,
        task_repository,
    ):
        # type: (ProjectRepository, AssetRepository, ShotRepository, TaskRepository) -> None
        self._project_repository = project_repository
        self._asset_repository = asset_repository
        self._shot_repository = shot_repository
        self._task_repository = task_repository

    def resolve(self, serialized_reference):
        # type: (SerializedTaskReference) -> TaskReference

        project = self._project_repository.find_by_name(
            serialized_reference.project_name
        )
        if not project:
            raise ValueError(
                'Could not find a project with name "{}"'.format(
                    serialized_reference.project_name
                )
            )

        if serialized_reference.entity_type == ReferenceEntityType.ASSET:
            entity = self._asset_repository.find_by_project_and_name(
                project.id, serialized_reference.entity_name
            )
            if not entity:
                raise ValueError(
                    'Could not find an asset with name "{}" for project with name "{}"'.format(
                        serialized_reference.entity_name,
                        serialized_reference.project_name,
                    )
                )
        elif serialized_reference.entity_type == ReferenceEntityType.SHOT:
            entity = self._shot_repository.find_by_project_and_name(
                project.id, serialized_reference.entity_name
            )
            if not entity:
                raise ValueError(
                    'Could not find a shot with name "{}" for project with name "{}"'.format(
                        serialized_reference.entity_name,
                        serialized_reference.project_name,
                    )
                )

        task = self._task_repository.find_by_project_and_name(
            project.id, serialized_reference.task_name
        )
        if not task:
            raise ValueError(
                'Could not find a task with name "{}" for project with name "{}"'.format(
                    serialized_reference.task_name, serialized_reference.project_name
                )
            )

        return TaskReference(
            project=project,
            entity_type=serialized_reference.entity_type,
            entity=entity,
            task=task,
        )
