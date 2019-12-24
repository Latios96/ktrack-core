from mongoengine import connect

from ktrack_api import config
from ktrack_api.mongo_impl.mongo_repositories import MongoPathEntryRepository


def get_path_entry_repository():
    connect("mongoeengine_test", host=config.read_connection_url())
    return MongoPathEntryRepository()
