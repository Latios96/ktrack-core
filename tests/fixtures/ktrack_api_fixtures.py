import pytest

from ktrack_api.mongo_impl import entities
from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl


@pytest.fixture
def ktrack_instance():
    """
    KtrackMongoImpl using mongomock. Will tear down and clean up database
    :return:
    """
    print "setting up ktrack instance dropping"
    impl =  KtrackMongoImpl('mongomock://localhost')
    yield impl
    print "tear down up ktrack instance dropping"
    for entity_name, entity_cls in entities.entities.iteritems():
        entity_cls.objects().all().delete()


@pytest.fixture
def ktrack_instance_non_dropping():
    """
    KtrackMongoImpl using mongomock. Will NOT tear down and clean up database
    :return:
    """
    return KtrackMongoImpl('mongomock://localhost')