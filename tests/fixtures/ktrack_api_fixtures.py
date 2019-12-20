import pytest
from mock import mock

from ktrack_api import ktrack
from ktrack_api.mongo_impl import entities
from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl

print("patching connection url")
ktrack._connection_url = "mongomock://localhost"


@pytest.fixture
def ktrack_instance():
    impl = KtrackMongoImpl("mongomock://localhost")
    yield impl
    for entity_name, entity_cls in entities.entities.items():
        entity_cls.objects().all().delete()


@pytest.fixture
def ktrack_instance_patched():
    impl = KtrackMongoImpl("mongomock://localhost")
    with mock.patch("ktrack_api.get_ktrack") as mock_get_ktrack:
        mock_get_ktrack.return_value = impl
        yield impl
    for entity_name, entity_cls in entities.entities.items():
        entity_cls.objects().all().delete()


@pytest.fixture
def ktrack_instance_non_dropping():
    return KtrackMongoImpl("mongomock://localhost")
