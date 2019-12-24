import logging
import os
import shutil
import uuid
from typing import Optional, Dict

from ktrack_api.config import read_connection_url
from ktrack_api.ktrack_impl import AbtractKtrackImpl

KtrackIdType = str
from ktrack_api.mongo_impl.ktrack_mongo_impl import KtrackMongoImpl

logger = logging.getLogger(__name__)

read_connection_url()
_connection_url = read_connection_url()


def get_ktrack():
    # type: () -> Ktrack
    connection_uri = _connection_url
    mongo_impl = KtrackMongoImpl(connection_uri)
    return Ktrack(mongo_impl)


class Ktrack(object):
    def __init__(self, impl):
        # type: (AbtractKtrackImpl) -> None
        self._impl = impl

    def create(self, entity_type, data={}):
        # type: (str, dict) -> dict
        assert isinstance(entity_type, str) or isinstance(entity_type, unicode)
        assert isinstance(data, dict)

        return self._impl.create(entity_type, data)

    def update(self, entity_type, entity_id, data):
        # type: (str, KtrackIdType, dict) -> None
        assert isinstance(entity_type, str) or isinstance(entity_type, unicode)
        assert isinstance(entity_id, str)
        assert isinstance(data, dict)

        return self._impl.update(entity_type, entity_id, data)

    def find(self, entity_type, filters=[]):
        # type: (str, list) -> list

        assert isinstance(entity_type, str) or isinstance(entity_type, unicode)
        assert isinstance(filters, list)

        return self._impl.find(entity_type, filters)

    def find_one(self, entity_type, entity_id):
        # type: (str, KtrackIdType) -> Optional[Dict]

        assert isinstance(entity_type, str) or isinstance(entity_type, unicode)
        assert isinstance(entity_id, str) or isinstance(entity_id, unicode)
        return self._impl.find_one(entity_type, entity_id)

    def delete(self, entity_type, entity_id):
        # type: (str, KtrackIdType) -> None

        assert isinstance(entity_type, str) or isinstance(entity_type, unicode)
        assert isinstance(entity_id, str)

        return self._impl.delete(entity_type, entity_id)

    def _get_thumbnail_path_template(self):
        # type: () -> str
        # todo make thumbnail folder editable in config, so its not hardcoded,
        return "M:/ktrack_thumbnails/thumbnail_{entity_type}_{entity_id}_{uuid}{ext}"

    def upload_thumbnail(self, entity_type, entity_id, path):
        # type: (str, KtrackIdType, str) -> None

        # todo should resize thumbnail
        thumbnail_path_template = self._get_thumbnail_path_template()
        thumbnail_path = thumbnail_path_template.format(
            entity_type=entity_type,
            entity_id=entity_id,
            uuid=uuid.uuid4(),
            ext=os.path.splitext(path)[1],
        )
        shutil.copy(path, thumbnail_path)
        self.update(entity_type, entity_id, {"thumbnail": {"path": thumbnail_path}})
