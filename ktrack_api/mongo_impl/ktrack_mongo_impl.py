from bson import ObjectId
from mongoengine import connect, DictField
from ktrack_api.mongo_impl import entities
from ktrack_api.Exceptions import EntityMissing, EntityNotFoundException


def _convert_to_dict(entity):
    obj_dict = {}

    obj_dict['type'] = entity.type

    for field in entity._fields_ordered:
        field_value = getattr(entity, field)

        if isinstance(field_value, ObjectId):
            obj_dict[field] = str(field_value)
        elif isinstance(field_value, DictField):
            obj_dict[field] = field.to_dict()
        else:
            if not field.startswith("_"):
                obj_dict[field] = field_value

    return obj_dict


class KtrackMongoImpl(object):
    """
    Mongo DB Implementation of the ktrack api interface. Uses mongoengine as a database mapper
    """

    def __init__(self, connection_uri):
        connect("mongoeengine_test",
                host=connection_uri)

    def create(self, entity_type, data={}):
        # type: (str, dict) -> dict
        """
        Creates a new entity instance of given type and applies given data.
        Returns new created entity
        :param entity_type: type of the new entity
        :param data: data for entity
        :return: newly created entity
        """
        # todo make sure that project names are unique
        try:
            entity_cls = entities.entities[entity_type.lower()]
        except KeyError:
            raise EntityMissing(entity_type)

        entity = entity_cls()

        for key, value in data.iteritems():
            setattr(entity, key, value)

        entity.save()

        return _convert_to_dict(entity)

    def update(self, entity_type, entity_id, data):
        try:
            entity_cls = entities.entities[entity_type]
        except KeyError:
            raise EntityMissing(entity_type)

        entity_candidates = entity_cls.objects(id = entity_id).all()

        if len(entity_candidates) == 0:
            raise EntityNotFoundException(str(entity_id))

        entity = entity_candidates[0]

        for key, value in data.iteritems():
            setattr(entity, key, value)

        entity.save()

    def find(self, entity_type, filters):
        try:
            entity_cls = entities.entities[entity_type]
        except KeyError:
            raise EntityMissing(entity_type)

        filter_dict={}

        if len(filters)>0:
            for f in filters:
                if isinstance(f[2], dict):
                    filter_dict["{}__id".format(f[0])] = f[2]['id']
                else:
                    field_name= f[0]
                    field_value= f[2]
                    filter_dict[field_name] = field_value

        entity_candidates = entity_cls.objects(**filter_dict).all()

        return [_convert_to_dict(x) for x in entity_candidates]




    def find_one(self, entity_type, entity_id):
        try:
            entity_cls = entities.entities[entity_type]
        except KeyError:
            raise EntityMissing(entity_type)

        entity_candidates = entity_cls.objects(id = entity_id).all()

        if len(entity_candidates) == 0:
            raise EntityNotFoundException(str(entity_id))

        return _convert_to_dict(entity_candidates[0])


    def delete(self, entity_type, entity_id):
        try:
            entity_cls = entities.entities[entity_type]
        except KeyError:
            raise EntityMissing(entity_type)

        entity_candidates = entity_cls.objects(id=entity_id).all()

        if len(entity_candidates) == 0:
            raise EntityNotFoundException(str(entity_id))

        entity_candidates.delete()
