import getpass


import pytest
from mongoengine import NotUniqueError

from ktrack_api.Exceptions import EntityMissing, EntityNotFoundException
from ktrack_api.mongo_impl.entities import Project, entities
from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl

SOME_OTHER_OBJECT_ID = "507f1f77bcf86cd799439011"

SOME_OBJECT_ID = "507f1f77bcf86cd799439012"


@pytest.fixture
def ktrack_instance():
    return KtrackMongoImpl('mongomock://localhost')


@pytest.fixture
def ktrack_instance_dropping():
    """
    Will drop all created entities after run
    :return:
    """
    impl =  KtrackMongoImpl('mongomock://localhost')
    yield impl
    print "clean"
    for entity_name, entity_cls in entities.iteritems():
        entity_cls.objects().all().delete()


def test_create(ktrack_instance_dropping):
    # type: (KtrackMongoImpl) -> None

    # create not existing entity
    with pytest.raises(EntityMissing):
        entity = ktrack_instance_dropping.create('projectaersrdtz')

    # test create existing entity
    entity = ktrack_instance_dropping.create('project')

    assert entity is not None

    assert type(entity) == dict

    assert entity['type'] == 'project'

    assert 'id' in entity.keys()

    assert entity['created_at']
    assert entity['updated_at']
    assert entity['created_by'] == getpass.getuser()

    entity_in_db = len(Project.objects(id=entity['id']))

    assert entity_in_db


def test_create_additional_data(ktrack_instance_dropping):
    # type: (KtrackMongoImpl) -> None

    # test create existing entity
    entity = ktrack_instance_dropping.create('project', {'name': 'my_lovely_project'})

    assert entity is not None

    assert type(entity) == dict

    assert entity['type'] == 'project'

    assert 'id' in entity.keys()

    assert entity['created_at']
    assert entity['updated_at']
    assert entity['created_by'] == getpass.getuser()
    assert entity['name'] == 'my_lovely_project'

    entity_in_db = len(Project.objects(id=entity['id']))

    assert entity_in_db


def test_update(ktrack_instance_dropping):
    # type: (KtrackMongoImpl) -> None

    # update not existing entity type
    with pytest.raises(EntityMissing):
        entity = ktrack_instance_dropping.update("projectaser", "aaaaaaaa", {})

    # update entity with useless id

    with pytest.raises(EntityNotFoundException):
        entity = ktrack_instance_dropping.update("project", SOME_OTHER_OBJECT_ID, {})

    # now test real update
    entity = ktrack_instance_dropping.create("project")

    old_update_time = entity['updated_at']

    thumbnail_dict = {'type': 'thumbnail', 'id': SOME_OBJECT_ID}

    ktrack_instance_dropping.update("project", entity['id'], {'thumbnail': thumbnail_dict})

    # now check if update was correct
    # get entity from db
    entity_in_db = Project.objects(id=entity['id'])

    # check that we have at least one entity
    assert len(entity_in_db) > 0

    entity = entity_in_db[0]

    # now check if values are correctly updated
    assert entity.thumbnail['type'] == 'thumbnail'
    assert entity.thumbnail['id'] == SOME_OBJECT_ID
    assert entity.updated_at > old_update_time


def test_delete(ktrack_instance_dropping):
    # type: (KtrackMongoImpl) -> None

    # test to delete not existing entity type
    with pytest.raises(EntityMissing):
        ktrack_instance_dropping.delete("<agt<eydrzuyaerz", SOME_OBJECT_ID)

    # test delete with not existing entity id
    with pytest.raises(EntityNotFoundException):
        ktrack_instance_dropping.delete('project', SOME_OBJECT_ID)

    # create entity to delete
    entity = ktrack_instance_dropping.create("project")

    entity_in_db = Project.objects(id=entity['id'])
    assert len(entity_in_db) > 0

    ktrack_instance_dropping.delete('project', entity['id'])

    # now check if object was deleted
    entity_in_db = Project.objects(id=entity['id'])
    assert len(entity_in_db) == 0


def test_find(ktrack_instance_dropping):
    # type: (KtrackMongoImpl) -> None

    # test to find not existing entity type
    with pytest.raises(EntityMissing):
        ktrack_instance_dropping.find("<agt<eydrzuyaerz", SOME_OBJECT_ID)

    ktrack_instance_dropping.create("shot", {'project': {'type': 'project', 'id': SOME_OBJECT_ID}})

    entities = ktrack_instance_dropping.find('shot', [['project', 'is', {'type': 'project', 'id': SOME_OBJECT_ID}]])

    assert len(entities) == 1


def test_find_field_value(ktrack_instance_dropping):
    SHOT_CODE = 'nivtrnitvrtni'
    ktrack_instance_dropping.create("shot", {'project': {'type': 'project', 'id': SOME_OBJECT_ID}, 'code': SHOT_CODE})

    entities = ktrack_instance_dropping.find('shot', [['code', 'is', SHOT_CODE]])

    assert len(entities) == 1


def test_find_one(ktrack_instance_dropping):
    # type: (KtrackMongoImpl) -> None

    # test to delete not existing entity type
    with pytest.raises(EntityMissing):
        ktrack_instance_dropping.find_one("<agt<eydrzuyaerz", SOME_OBJECT_ID)

    # test delete with not existing entity id
    with pytest.raises(EntityNotFoundException):
        ktrack_instance_dropping.find_one('project', SOME_OBJECT_ID)

    # create one object

    entity = ktrack_instance_dropping.create('project')

    _entity = ktrack_instance_dropping.find_one('project', entity['id'])

    assert entity['id'] == _entity['id']

"""
def test_project_name_unique(ktrack_instance_dropping):
    # type: (KtrackMongoImpl) -> None

    ktrack_instance_dropping.create("project", {'name': 'my_awesome_project_name'})

    with pytest.raises(NotUniqueError):
        ktrack_instance_dropping.create("project", {'name': 'my_awesome_project_name'})"""
