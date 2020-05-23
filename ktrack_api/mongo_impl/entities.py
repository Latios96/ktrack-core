import datetime
import getpass

from mongoengine import (
    signals,
    Document,
    DateTimeField,
    StringField,
    DictField,
    IntField,
)
from typing import Dict


def update_modified(sender, document):
    print("update_modified for {}", document)
    document.updated_at = datetime.datetime.now()


signals.pre_save.connect(update_modified)

entities = {}  # type: Dict[str, NonProjectEntity]


def register_entity(name, entity_cls):
    """
    Registers a new domain_entity by their name
    :param name: domain_entity name, all names are handled in lower-case
    :param entity_cls: class of domain_entity to register
    :return:
    """
    entities[name.lower()] = entity_cls


class NonProjectEntity(Document):
    created_at = DateTimeField(default=datetime.datetime.now())
    created_by = StringField(default=getpass.getuser())
    updated_at = DateTimeField()
    type = "NonProjectEntity"
    thumbnail = DictField()  # dict like {'path': thumbnail_path}

    meta = {"abstract": True}


class ProjectEntity(NonProjectEntity):
    project = DictField(required=True)

    meta = {"abstract": True}


class Project(NonProjectEntity):
    type = "project"
    # name = StringField(unique=True) todo make domain_entity name unique and fix mocked version, tests will fail otherwise
    name = StringField()


register_entity("project", Project)


class Asset(ProjectEntity):
    type = "asset"
    code = StringField()
    asset_type = StringField()  # todo make asset_type required


register_entity("asset", Asset)


class Shot(ProjectEntity):
    type = "shot"
    code = StringField()
    cut_in = IntField()
    cut_out = IntField()
    cut_duration = IntField()


register_entity("shot", Shot)


class PathEntry(NonProjectEntity):
    type = "path_entry"
    path = StringField(required=True)
    context = DictField(required=True)


register_entity("path_entry", PathEntry)


class Task(ProjectEntity):
    type = "task"
    step = StringField()
    name = StringField()
    entity = DictField(required=True)
    assigned = DictField()  # todo assign mulitple people to one task


register_entity("task", Task)


class WorkFile(ProjectEntity):
    type = "workfile"
    name = StringField()
    entity = DictField()
    path = StringField(required=True)
    comment = StringField()
    version_number = IntField()
    created_from = DictField(default=None)


register_entity("workfile", WorkFile)


class User(NonProjectEntity):
    name = StringField()
    first_name = StringField()
    second_name = StringField()


register_entity("user", User)
