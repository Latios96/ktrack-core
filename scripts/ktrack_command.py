# init:
# if project:
#   checken ob es namen gibt, dann project in db erstellen und dann initialisieren
# else:
#   checken ob aktueller ordner einen context hat, wenn ja, dann context holen, wenn nicht, abbruch
#   neuen entity erstellen und mit context richtig verlinken, dann initialisieren
import argparse
import os
import pprint

import fire
from tabulate import tabulate

import ktrack_api
import kttk
from kttk import logger


# todo use python fire
def execute_cmd(parsed_args):
    if parsed_args.init:
        logger.info("init cmd")
        logger.info("Connecting to database..")
        kt = ktrack_api.get_ktrack()
        entity_type, entity_name = parsed_args.init[1:]

        if entity_type == 'project':
            logger.info("initialise project")
            logger.info("create project in database..")

            project_data = {}
            project_data['name'] = entity_name

            project = kt.create("project", project_data)

            logger.info("Created project {} with id {}".format(project['name'], project['id']))

            logger.info("initialise project on disk..")
            kttk.init_entity('project', project['id'])

            logger.info("{entity_type} with id {entity_id} initialised. Done.".format(entity_type='project',
                                                                                      entity_id=project['id']))
        else:
            is_asset = entity_type == 'asset'
            is_task = entity_type == 'task'

            if is_asset:
                if not parsed_args.asset_type:
                    print "no asset type"
                    return

            if is_task:
                if not parsed_args.task_step:
                    raise Exception()

            logger.info("initialise {}".format(entity_type))

            current_location = os.getcwd()
            # current_location = r"M:\Projekte\2018\my_awesome_project"
            logger.info("Restore context from location {}..".format(current_location))

            context = kttk.context_from_path(current_location)

            logger.info("Context is {context}".format(context=context))

            logger.info("create {} in database..".format(entity_type))

            entity_data = {}
            entity_data['code'] = entity_name
            entity_data['project'] = context.project

            if is_asset:
                entity_data['asset_type'] = parsed_args.asset_type

            if is_task:
                entity_data['name'] = entity_name
                entity_data['step'] = parsed_args.task_step
                entity_data['entity'] = context.entity

                entity_data['assigned'] = {'type': 'user',
                                           'id': '5af33abd6e87ff056014967a'}  # todo dont hardcode user id

            entity = kt.create(entity_type, entity_data)

            logger.info("created {entity_type} {entity_name} with id {entity_id}.".format(entity_type=entity['type'],
                                                                                          entity_name=entity.get(
                                                                                              'code') if entity.get(
                                                                                              'code') else entity[
                                                                                              'name'],
                                                                                          entity_id=entity['id']))

            logger.info("initialise project on disk..")

            kttk.init_entity(entity_type, entity['id'])

            logger.info("{entity_type} with id {entity_id} initialised. Done.".format(entity_type=entity['type'],
                                                                                      entity_id=entity['id']))


def get_name_or_code(entity):
    # type: (dict) -> str
    """
    Checks if given entity has a name or code and returns the name or code
    Some entities have a code to identify them (shots for example), some have names (project)
    :param entity: entity to extract the name from
    :return: entity['name'] if entity has name, else entity['code']
    """
    # todo move to some util package and add tests
    has_name = entity.get("name")
    has_code = entity.get("code")

    if has_name:
        return entity['name']
    elif has_code:
        return entity['code']


def create(entity_type, name, project=None):
    # todo implement create
    print "creation entity of type {} with name {} for project {}".format(entity_type, name, project)


def find_one(entity_type, entity_id):
    """
    Finds the given entity in the database and pretty prints it
    :param entity_type: type of the entity
    :param entity_id: id of the entity
    :return: None
    """
    kt = ktrack_api.get_ktrack()

    entity = None
    try:
        # todo remove exception handling when find_one does not throw an exception anymore
        entity = kt.find_one(entity_type, entity_id)

    except ktrack_api.Exceptions.EntityNotFoundException:
        pass

    if entity:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(entity)
    else:
        print 'Entity of type "{}" and id "{}" not found..'.format(entity_type, entity_id)


# todo add sort by option
# todo add tests
# todo test link_entity_type and link_entity_id
def show(entity_type, link_entity_type=None, link_entity_id=None):
    # type: (str, str, str) -> None

    # make sure entity type is lowercase
    entity_type = entity_type.lower()

    entities = None

    kt = ktrack_api.get_ktrack()

    try:
        # if we have a link_entity_type and link_entity_id, we use a filter
        if link_entity_type and link_entity_id:
            # make sure link_entity_type is also lowercase
            link_entity_type = link_entity_type.lower()
            entities = kt.find(entity_type, [['link', 'is', {'type': link_entity_type, 'id': link_entity_id}]])

        # otherwise we get all entities of this type
        else:
            entities = kt.find(entity_type, [])

    except ktrack_api.Exceptions.EntityMissing:
        print "Entity type {} does not exist".format(entity_type)
        return

    # make sure we got at least one entits
    got_entities = entities is not None and len(entities) > 0

    if got_entities:
        # generate table

        entities = sorted(entities, key=get_name_or_code)

        # get all dict keys from first entity and sort them
        first_entity = entities[0]
        headers = ['id', get_name_or_code(first_entity), 'created_at',
                   'created_by']

        table = []

        for entity in entities:
            entry = (entity['id'], get_name_or_code(entity), entity['created_at'],
                     entity['created_by'])

            table.append(entry)

        print tabulate(table, headers=headers)

    else:
        print "No entities of type {} found..".format(entity_type)


def context(path=os.getcwd()):
    # todo implement context
    print "Context for {} is {}".format(path, "<Context>")


def update(entity_type, entity_id, data):
    # FIXME not working yet
    print "updating entity of type {} with id {} with data {}".format(entity_type, entity_id, data)


def main():
    fire.Fire({
        'create': create,
        'find_one': find_one,
        'show': show,
        'context': context
        # TODO add update
    })


if __name__ == '__main__':
    main()
