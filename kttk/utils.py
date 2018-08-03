def entity_id_dict(entity):
    # type: (dict) -> dict
    """
    Returns a new dict with only type and id keys matching given entity
    :param entity: entity dict with at least type and id
    :return: new dict with only type and id keys matching given entity
    """
    if entity != None:
        return {'type': entity['type'], 'id': entity['id']}
    return None