import pytest
from mock import mock

from ktrack_api import ktrack
from ktrack_api.mongo_impl import entities
from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl

print "patching connection url"
ktrack._connection_url = 'mongomock://localhost'


@pytest.fixture
def ktrack_instance():
    """
    KtrackMongoImpl using mongomock Will tear down and clean up database
    :return:
    """
    print "setting up ktrack instance dropping"
    impl =  KtrackMongoImpl('mongomock://localhost')
    yield impl
    print "tear down up ktrack instance dropping"
    for entity_name, entity_cls in entities.entities.iteritems():
        entity_cls.objects().all().delete()

@pytest.fixture
def ktrack_instance_patched():
    """
    KtrackMongoImpl using mongomock, will also mock ktrack_api.get_ktrack() Will tear down and clean up database
    :return:
    """
    print "setting up ktrack instance dropping"
    impl =  KtrackMongoImpl('mongomock://localhost')
    with mock.patch('ktrack_api.get_ktrack') as mock_get_ktrack:
        mock_get_ktrack.return_value = impl
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