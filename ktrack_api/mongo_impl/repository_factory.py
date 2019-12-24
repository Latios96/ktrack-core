from mongoengine import connect

from ktrack_api.repositories import PathEntryRepository
from ktrack_api.mongo_impl.mongo_repositories import MongoPathEntryRepository


def get_mongo_path_entry_repository(connection_uri):
    # type: (str) -> PathEntryRepository
    connect("mongoeengine_test", host=connection_uri)
    return MongoPathEntryRepository()
