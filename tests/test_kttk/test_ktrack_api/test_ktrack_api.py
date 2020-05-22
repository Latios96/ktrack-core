import datetime
import getpass
import pytest
from bson import ObjectId
from mongoengine import Document, DateTimeField, StringField, DictField

from ktrack_api.exceptions import EntityMissing, EntityNotFoundException
from ktrack_api.mongo_impl.entities import Project, entities
from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl, _convert_to_dict

SOME_OTHER_OBJECT_ID = "507f1f77bcf86cd799439011"

SOME_OBJECT_ID = "507f1f77bcf86cd799439012"


class TestEntity(Document):
    time_field = DateTimeField(default=datetime.datetime.now())
    string_field = StringField()
    type = "NonProjectEntity"
    dict_field = DictField()
    id = ObjectId()


def test_convert_to_dict(ktrack_instance):
    entity = TestEntity()
    entity.string_field = "value"
    entity.dict_field["bla"] = 123
    entity.save()

    entity_dict = _convert_to_dict(entity)

    assert entity_dict["type"] == "NonProjectEntity"
    assert isinstance(entity_dict["id"], str)
    assert isinstance(entity_dict["dict_field"], dict)
    assert isinstance(entity_dict["string_field"], str)
    assert isinstance(entity_dict["time_field"], datetime.datetime)


def test_create(ktrack_instance):
    # type: (KtrackMongoImpl) -> None

    # create not existing entity
    with pytest.raises(EntityMissing):
        entity = ktrack_instance.create("projectaersrdtz")

    # test create existing entity
    entity = ktrack_instance.create("project")

    assert entity is not None

    assert type(entity) == dict

    assert entity["type"] == "project"

    assert "id" in entity.keys()

    assert entity["created_at"]
    assert entity["updated_at"]
    assert entity["created_by"] == getpass.getuser()

    entity_in_db = len(Project.objects(id=entity["id"]))

    assert entity_in_db


def test_create_additional_data(ktrack_instance):
    # type: (KtrackMongoImpl) -> None

    # test create existing entity
    entity = ktrack_instance.create("project", {"name": "my_lovely_project"})

    assert entity is not None

    assert type(entity) == dict

    assert entity["type"] == "project"

    assert "id" in entity.keys()

    assert entity["created_at"]
    assert entity["updated_at"]
    assert entity["created_by"] == getpass.getuser()
    assert entity["name"] == "my_lovely_project"

    entity_in_db = len(Project.objects(id=entity["id"]))

    assert entity_in_db


def test_update(ktrack_instance):
    # type: (KtrackMongoImpl) -> None

    # update not existing entity type
    with pytest.raises(EntityMissing):
        entity = ktrack_instance.update("projectaser", "aaaaaaaa", {})

    # update entity with useless id

    with pytest.raises(EntityNotFoundException):
        entity = ktrack_instance.update("project", SOME_OTHER_OBJECT_ID, {})

    # now test real update
    entity = ktrack_instance.create("project")

    old_update_time = entity["updated_at"]

    thumbnail_dict = {"type": "thumbnail", "id": SOME_OBJECT_ID}

    ktrack_instance.update("project", entity["id"], {"thumbnail": thumbnail_dict})

    # now check if update was correct
    # get entity from db
    entity_in_db = Project.objects(id=entity["id"])

    # check that we have at least one entity
    assert len(entity_in_db) > 0

    entity = entity_in_db[0]

    # now check if values are correctly updated
    assert entity.thumbnail["type"] == "thumbnail"
    assert entity.thumbnail["id"] == SOME_OBJECT_ID
    import time

    time.sleep(1)
    assert entity.updated_at != old_update_time


def test_delete(ktrack_instance):
    # type: (KtrackMongoImpl) -> None

    # test to delete not existing entity type
    with pytest.raises(EntityMissing):
        ktrack_instance.delete("<agt<eydrzuyaerz", SOME_OBJECT_ID)

    # test delete with not existing entity id
    with pytest.raises(EntityNotFoundException):
        ktrack_instance.delete("project", SOME_OBJECT_ID)

    # create entity to delete
    entity = ktrack_instance.create("project")

    entity_in_db = Project.objects(id=entity["id"])
    assert len(entity_in_db) > 0

    ktrack_instance.delete("project", entity["id"])

    # now check if object was deleted
    entity_in_db = Project.objects(id=entity["id"])
    assert len(entity_in_db) == 0


def test_find(ktrack_instance):
    # type: (KtrackMongoImpl) -> None

    # test to find not existing entity type
    with pytest.raises(EntityMissing):
        ktrack_instance.find("<agt<eydrzuyaerz", SOME_OBJECT_ID)

    ktrack_instance.create(
        "shot", {"project": {"type": "project", "id": SOME_OBJECT_ID}}
    )

    entities = ktrack_instance.find(
        "shot", [["project", "is", {"type": "project", "id": SOME_OBJECT_ID}]]
    )

    assert len(entities) == 1


def test_find_field_value(ktrack_instance):
    SHOT_CODE = "nivtrnitvrtni"
    ktrack_instance.create(
        "shot",
        {"project": {"type": "project", "id": SOME_OBJECT_ID}, "code": SHOT_CODE},
    )

    entities = ktrack_instance.find("shot", [["code", "is", SHOT_CODE]])

    assert len(entities) == 1


def test_find_one(ktrack_instance):
    # type: (KtrackMongoImpl) -> None

    # test to delete not existing entity type
    with pytest.raises(EntityMissing):
        ktrack_instance.find_one("<agt<eydrzuyaerz", SOME_OBJECT_ID)

    # test delete with not existing entity id
    assert ktrack_instance.find_one("project", SOME_OBJECT_ID) is None

    # create one object

    entity = ktrack_instance.create("project")

    _entity = ktrack_instance.find_one("project", entity["id"])

    assert entity["id"] == _entity["id"]


"""
def test_project_name_unique(ktrack_instance):
    # type: (KtrackMongoImpl) -> None

    ktrack_instance.create("project", {'name': 'my_awesome_project_name'})

    with pytest.raises(NotUniqueError):
        ktrack_instance.create("project", {'name': 'my_awesome_project_name'})"""
