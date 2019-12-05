from ktrack_api.ktrack import KtrackIdType


class EntityMissing(Exception):

    def __init__(self, entity_type):
        super(EntityMissing, self).__init__("No entity of given type {} exists!!!".format(entity_type))


class EntityNotFoundException(Exception):

    def __init__(self, entity_id):
        # type: (KtrackIdType) -> None
        super(EntityNotFoundException, self).__init__("No entity with id {} exists".format(entity_id))
