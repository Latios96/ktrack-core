from ktrack_api.ktrack import KtrackIdType


class EntityMissing(Exception):
    """
    Exception thrown when someone tries to access an entity type which does not exist in ktrack
    """

    def __init__(self, entity_type):
        super(EntityMissing, self).__init__("No entity of given type {} exists!!!".format(entity_type))


class EntityNotFoundException(Exception):
    """
    Exception thrown when no entity with given id exists in database
    """

    def __init__(self, entity_id):
        # type: (KtrackIdType) -> None
        super(EntityNotFoundException, self).__init__("No entity with id {} exists".format(entity_id))
