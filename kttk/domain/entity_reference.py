import attr


@attr.s
class EntityReference(object):
    project_name = attr.ib(type=str)
    entity_name = attr.ib(type=str)

    def __str__(self):
        return "{}:{}".format(self.project_name, self.entity_name)

    @staticmethod
    def parse(entity_reference):
        # type: (str) -> EntityReference
        if not entity_reference:
            raise ValueError("Can not parse from '{}'!".format(entity_reference))
        project_name, entity_name = entity_reference.split(":")
        return EntityReference(project_name, entity_name)
