from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl


def get_ktrack():
    # connection_uri = ("mongodb://ktrack_admin:mErGSKW2hFFuYceo@cluster0-shard-00-00-2k1zb.mongodb.net:27017,cluster0-shard-00-01-2k1zb.mongodb.net:27017,cluster0-shard-00-02-2k1zb.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    connection_uri="mongodb://localhost:27090/ktrack"
    mongo_impl = KtrackMongoImpl(connection_uri)
    return Ktrack(mongo_impl)


class Ktrack(object):

    def __init__(self, impl):
        # type: (Ktrack) -> object
        self._impl = impl

    def create(self, entity_type, data={}):
        # type: (str, dict) -> dict
        """
        Creates a new entity instance of given type and applies given data.
        Returns new created entity
        :param entity_type: type of the new entity
        :param data: data for entity
        :return: newly created entity
        """
        return self._impl.create(entity_type, data)

    def update(self, entity_type, entity_id, data):
        # todo add types and docs
        return self._impl.update(entity_type, entity_id, data)

    def find(self, entity_type, filters):
        # todo add types and docs
        return self._impl.find(entity_type, filters)

    def find_one(self, entity_type, entity_id):
        # todo add types and docs
        return self._impl.find_one(entity_type, entity_id)

    def delete(self, entity_type, entity_id):
        # todo add types and docs
        return self._impl.delete(entity_type, entity_id)

    def upload_thumbnail(self):
        raise NotImplementedError() # todo implement this, should copy thumbnail image to some location
