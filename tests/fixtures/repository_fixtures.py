import pytest
from mongoengine import connect

from ktrack_api.mongo_impl.entities import (
    Project as MongoProject,
    Asset as MongoAsset,
    PathEntry as MongoPathEntry,
)
from ktrack_api.mongo_impl.mongo_repositories import (
    MongoProjectRepository,
    MongoAssetRepository,
    MongoPathEntryRepository,
)


@pytest.fixture
def mongo_project_repository():
    connect("mongoeengine_test", host="mongomock://localhost")
    MongoProject.objects().all().delete()
    return MongoProjectRepository()


@pytest.fixture
def mongo_asset_repository():
    connect("mongoeengine_test", host="mongomock://localhost")
    MongoAsset.objects().all().delete()
    return MongoAssetRepository()


@pytest.fixture
def mongo_path_entry_repository():
    connect("mongoeengine_test", host="mongomock://localhost")
    MongoPathEntry.objects().all().delete()
    return MongoPathEntryRepository()
