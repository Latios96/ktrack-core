class EntityMissing(Exception):
    # todo add doc
    def __init__(self, entity_type):
        super(EntityMissing, self).__init__("No entity of given type {} exists!!!".format(entity_type))


class EntityNotFoundException(Exception):
    # todo add doc
    def __init__(self, entity_id):
        super(EntityNotFoundException, self).__init__("No entity with id {} exists".format(entity_id))
