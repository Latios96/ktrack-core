from typing import Optional, Dict


def entity_id_dict(entity):
    # type: (dict) -> Optional[Dict]
    if entity:
        return {"type": entity["type"], "id": entity["id"]}
    return None


def frozen_entity_id_dict(entity):
    # type: (dict) -> FrozenDict
    if entity is not None:
        return FrozenDict({"type": entity["type"], "id": entity["id"]})
    return None


class FrozenDict(dict):
    def __init__(self, data):
        # type: (dict) -> None
        super(FrozenDict, self).__init__()
        for key, value in data.items():
            super(FrozenDict, self).__setitem__(key, value)

    def __setitem__(self, item):
        raise TypeError("This dict is frozen")
