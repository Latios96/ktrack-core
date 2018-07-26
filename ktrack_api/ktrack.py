import os
import shutil
import uuid

from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl

_connection_url = "mongodb://localhost:27090/ktrack"

def get_ktrack():
    """
    Factory method which returns a new Ktrack instance with the current implementation.
    Change here if you want to use a different implementation
    :return:
    """
    # type: () -> Ktrack
    # connection_uri = ("mongodb://ktrack_admin:mErGSKW2hFFuYceo@cluster0-shard-00-00-2k1zb.mongodb.net:27017,cluster0-shard-00-01-2k1zb.mongodb.net:27017,cluster0-shard-00-02-2k1zb.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    connection_uri = _connection_url
    mongo_impl = KtrackMongoImpl(connection_uri)
    return Ktrack(mongo_impl)


class Ktrack(object):

    def __init__(self, impl):
        # type: (Ktrack) -> None
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
        assert (isinstance(entity_type, str) or isinstance(entity_type, unicode))
        assert isinstance(data, dict)

        return self._impl.create(entity_type, data)

    def update(self, entity_type, entity_id, data):
        # type: (str, object, dict) -> None
        """
        Update entity of given type with given id with given data
        :param entity_type: type of entity to update
        :param entity_id: id of entity to update
        :param data: dict with data to update
        :return: None
        """
        assert (isinstance(entity_type, str) or isinstance(entity_type, unicode))
        assert isinstance(entity_id, str)
        assert isinstance(data, dict)

        return self._impl.update(entity_type, entity_id, data)

    def find(self, entity_type, filters=[]):
        # type: (object, object) -> object
        # type: (str, list) -> list
        """
        Finds an entity of given type with matching filters
        :param entity_type:
        :param filters: [[field_name, 'is', field_value]] or [] is currently supported, default is []
        :return: list of matching entities, empty list if no matching entity found
        """
        assert (isinstance(entity_type, str) or isinstance(entity_type, unicode))
        assert isinstance(filters, list)

        return self._impl.find(entity_type, filters)

    def find_one(self, entity_type, entity_id):
        # type: (str, str) -> dict
        """
        Finds one entity of given type and id
        :param entity_type: type of entity
        :param entity_id: id of entity
        :return: entity dict
        """
        assert (isinstance(entity_type, str) or isinstance(entity_type, unicode))
        assert (isinstance(entity_id, str) or isinstance(entity_id, unicode))
        return self._impl.find_one(entity_type, entity_id)

    def delete(self, entity_type, entity_id):
        # type: (str, str) -> None
        """
        Deleted entity of given type with given id
        :param entity_type: type of entity
        :param entity_id: id of entity
        :return: None
        """
        assert (isinstance(entity_type, str) or isinstance(entity_type, unicode))
        assert isinstance(entity_id, str)

        return self._impl.delete(entity_type, entity_id)

    def _get_thumbnail_path_template(self):
        # type: () -> str
        # todo make thumbnail folder editable in config, so its not hardcoded,
        return "M:/ktrack_thumbnails/thumbnail_{entity_type}_{entity_id}_{uuid}{ext}"

    def upload_thumbnail(self, entity_type, entity_id, path):
        # type: (str, str, str) -> None
        """
        Uploads the image at given path to ktrack. "Uploading" means copy to a location on disk specified in _get_thumbnail_path_template.
        File name will be like thumbnail_{entity_type}_{entity_id}_{uuid}{ext}
        Updates the thumbnail field on the given entity
        :param entity_type: type of entity to upload the thumbnail for, for example project
        :param entity_id: id of the entity to upload the thumbnail dor
        :param path: path of the source image
        :return: None
        """
        # todo should resize thumbnail
        thumbnail_path_template = self._get_thumbnail_path_template()
        thumbnail_path = thumbnail_path_template.format(entity_type=entity_type,
                                                        entity_id=entity_id,
                                                        uuid=uuid.uuid4(),
                                                        ext=os.path.splitext(path)[1])
        shutil.copy(path, thumbnail_path)
        self.update(entity_type, entity_id, {'thumbnail': {'path': thumbnail_path}})
