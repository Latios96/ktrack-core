import frozendict
from typing import Optional, Dict


def entity_id_dict(entity):
    # type: (dict) -> Optional[Dict]
    """
    Returns a new dict with only type and id keys matching given entity
    :param entity: entity dict with at least type and id
    :return: new dict with only type and id keys matching given entity
    """
    if entity:
        return {'type': entity['type'], 'id': entity['id']}
    return None


def frozen_entity_id_dict(entity):
    # type: (dict) -> frozendict
    """
    Returns a new frozen dict with only type and id keys matching given entity
    :param entity: entity dict with at least type and id
    :return: new dict with only type and id keys matching given entity
    """
    if entity != None:
        return FrozenDict({'type': entity['type'], 'id': entity['id']})
    return None

# todo WTF is this?
class FrozenDict(dict):
    """
    A dictionary whoch does not support modification
    """

    def __init__(self, data):
        # type: (dict) -> None
        super(FrozenDict, self).__init__()
        for key, value in data.items():
            super(FrozenDict, self).__setitem__(key, value)

    def __setitem__(self, item):
        raise TypeError("This dict is frozen")
