from kttk.references.entity_types import ReferenceEntityType
from kttk.references.task_reference import SerializedTaskReference


class SerializedTaskReferenceParser(object):
    def parse(self, string):
        # type: (str) -> SerializedTaskReference
        (project_name, entity_type, entity_name, task_name) = string.split(":")

        if not entity_type in ["a", "sh"]:
            raise ValueError('Invalid entity type: "{}"'.format(entity_type))

        return SerializedTaskReference(
            project_name=project_name,
            entity_type=ReferenceEntityType.ASSET
            if entity_type == "a"
            else ReferenceEntityType.SHOT,
            entity_name=entity_name,
            task_name=task_name,
        )
