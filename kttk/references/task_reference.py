import attr

from kttk.domain.entities import Project, ProjectEntity, Task, Workfile
from kttk.references.entity_types import ReferenceEntityType


@attr.s
class SerializedTaskReference(object):
    project_name = attr.ib(type=str)
    entity_type = attr.ib(type=str)
    entity_name = attr.ib(type=str)
    task_name = attr.ib(type=str)


@attr.s
class TaskReference(object):
    project = attr.ib(type=Project)
    entity_type = attr.ib(type=ReferenceEntityType)
    entity = attr.ib(type=ProjectEntity)
    task = attr.ib(type=Task)
