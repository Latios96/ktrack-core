import datetime
import getpass

from mongoengine import signals, Document, DateTimeField, StringField, DictField, IntField


def update_modified(sender, document):
    document.updated_at = datetime.datetime.now()


signals.pre_save.connect(update_modified)

entities = {}


def register_entity(name, entity_cls):
    """
    Registers a new entity by their name
    :param name: entity name, all names are handled in lower-case
    :param entity_cls: class of entity to register
    :return:
    """
    entities[name.lower()] = entity_cls


class NonProjectEntity(Document):
    created_at = DateTimeField(default=datetime.datetime.now())
    created_by = StringField(default=getpass.getuser())
    updated_at = DateTimeField()
    type = 'NonProjectEntity'
    thumbnail = DictField()

    meta = {'allow_inheritance': True,
            'collection': 'ktrack_api_entities'}

    # currently unused
    """def to_link(self):
        return {'type': self.type, 'id': self.id} # todo add test"""


class ProjectEntity(NonProjectEntity):
    project = DictField(required=True)


class Project(NonProjectEntity):
    type = 'project'
    name = StringField()


register_entity('project', Project)


class Asset(ProjectEntity):
    type = 'asset'
    code = StringField()
    asset_type = StringField()


register_entity('asset', Asset)


class Shot(ProjectEntity):
    type = 'shot'
    code = StringField()
    cut_in = IntField()
    cut_out = IntField()
    cut_duration = IntField()


register_entity('shot', Shot)


class PathEntry(NonProjectEntity):
    type = 'path_entry'
    path = StringField()
    context = DictField()


register_entity('path_entry', PathEntry)


class Task(ProjectEntity):
    type = 'task'
    step = StringField()
    name = StringField()
    entity = DictField(required=True)


register_entity('task', Task)


class WorkFile(ProjectEntity):
    type = 'workfile'
    name = StringField()
    entity = DictField()
    path = StringField(required=True)
    comment = StringField()
    version_number = IntField()


register_entity('workfile', WorkFile)
