from typing import List, Optional, Dict


class AbtractKtrackImpl(object):
    def __init__(self, connection_uri):
        # type: (str) -> None
        pass

    def create(self, entity_type, data={}):
        # type: (str, dict) -> dict
        raise NotImplementedError()

    def update(self, entity_type, entity_id, data):
        # type: (str, str, dict) -> None
        raise NotImplementedError()

    def find(self, entity_type, filters):
        # type: (str, list) -> List[dict]
        raise NotImplementedError()

    def find_one(self, entity_type, entity_id):
        # type: (str, str) -> Optional[Dict]
        raise NotImplementedError()

    def delete(self, entity_type, entity_id):
        # type: (str, str) -> None
        raise NotImplementedError()
