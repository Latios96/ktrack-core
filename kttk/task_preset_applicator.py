import kttk
from kttk.domain.entities import Task, EntityLink


class TaskPresetApplicator(object):
    def __init__(self, task_repository, init_entity):
        self._task_repository = task_repository
        self._init_entity = init_entity

    def apply(self, entity_type, project_id, entity_id):
        # get task presets for entity
        presets = kttk.get_task_presets(entity_type)

        for preset in presets:
            kttk.logger.info(
                "Creating task {} of step {}".format(preset["name"], preset["step"])
            )
            task = Task(
                project=project_id,
                entity=EntityLink(type=entity_type, id=entity_id),
                name=preset["name"],
                step=preset["step"],
            )

            task = self._task_repository.save(task)

            self._init_entity("task", task.id)
