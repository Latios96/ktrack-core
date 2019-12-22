import ktrack_api

# todo remove
from ktrack_api.mongo_impl.mongo_repositories import MongoProjectRepository

kt = ktrack_api.get_ktrack()

project_repository = MongoProjectRepository()
