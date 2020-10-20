from ktrack_api.repositories import (
    ProjectRepository,
    AssetRepository,
    ShotRepository,
    TaskRepository,
    WorkfileRepository,
)
from kttk.domain.entities import VersionNumber
from kttk.references.entity_types import ReferenceEntityType
from kttk.references.workfile_reference import (
    SerializedWorkfileReference,
    WorkfileReference,
)


class WorkfileReferenceResolver(object):
    def __init__(
        self,
        project_repository,
        asset_repository,
        shot_repository,
        task_repository,
        workfile_repository,
    ):
        # type: (ProjectRepository, AssetRepository, ShotRepository, TaskRepository, WorkfileRepository) -> None
        self._project_repository = project_repository
        self._asset_repository = asset_repository
        self._shot_repository = shot_repository
        self._task_repository = task_repository
        self._workfile_repository = workfile_repository

    def resolve(self, serialized_reference):
        # type: (SerializedWorkfileReference) -> WorkfileReference

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

        if serialized_reference.version_identifier == "latest":
            workfile = self._workfile_repository.find_by_task_latest(task.id)
        else:
            version_number = VersionNumber(serialized_reference.version_identifier)
            workfile = self._workfile_repository.find_by_task_and_version_number(
                task.id, version_number
            )
        if not workfile:
            raise ValueError(
                'Could not find a Workfile with version identifier "{}" for project with name "{}"'.format(
                    serialized_reference.version_identifier,
                    serialized_reference.project_name,
                )
            )

        return WorkfileReference(
            project=project,
            entity_type=serialized_reference.entity_type,
            entity=entity,
            task=task,
            workfile=workfile,
        )
