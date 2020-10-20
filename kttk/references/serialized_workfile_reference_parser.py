from kttk.domain.entities import VersionNumber
from kttk.references.entity_types import ReferenceEntityType
from kttk.references.workfile_reference import SerializedWorkfileReference


class SerializedWorkfileReferenceParser(object):
    def parse(self, string):
        # type: (str) -> SerializedWorkfileReference
        (
            project_name,
            entity_type,
            entity_name,
            task_name,
            version_idenfier,
        ) = string.split(":")

        if not (version_idenfier == "latest" or VersionNumber(version_idenfier)):
            raise ValueError(
                'Invalid version identifier: "{}"'.format(version_idenfier)
            )
        if not entity_type in ["a", "sh"]:
            raise ValueError('Invalid entity type: "{}"'.format(entity_type))

        return SerializedWorkfileReference(
            project_name=project_name,
            entity_type=ReferenceEntityType.ASSET
            if entity_type == "a"
            else ReferenceEntityType.SHOT,
            entity_name=entity_name,
            task_name=task_name,
            version_identifier=version_idenfier,
        )
