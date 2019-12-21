import json
import os
import pprint

import fire
from tabulate import tabulate

import ktrack_api
import kttk
from ktrack_api.exceptions import EntityMissing
from kttk import logger


def print_result(result):
    """
    Wrapper around print for better testing
    :param result:
    :return:
    """
    print(result)


# todo write tests


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
        return entity["name"]
    elif has_code:
        return entity["code"]


def create(entity_type, entity_name, project_id=None, asset_type=None, task_step=None):
    """
    Creates a new entity if given type in database and initialises it in disk kttk.init_entity
    :param entity_type: type of the new entity to create
    :param entity_name: name the new entity will get, will be used for code if entity has no name
    :param project_id: optional, will link project entity to project with this id
    :param asset_type: type a newly created asset will get
    :param task_step: step a newly created task will get
    :return: None
    """
    # init:
    # if project:
    #   checken ob es namen gibt, dann project in db erstellen und dann initialisieren
    # else:
    #   checken ob aktueller ordner einen context hat, wenn ja, dann context holen, wenn nicht, abbruch
    #   neuen entity erstellen und mit context richtig verlinken, dann initialisieren
    # todo add some more documentation
    logger.info(
        "creation entity of type {} with name {} for project {}".format(
            entity_type, entity_name, project_id
        )
    )
    logger.info("init cmd")
    logger.info("Connecting to database..")
    kt = ktrack_api.get_ktrack()

    if entity_type == "project":
        logger.info("initialise project")
        logger.info("create project in database..")

        project_data = {}
        project_data["name"] = entity_name

        project = kt.create("project", project_data)

        logger.info(
            "Created project {} with id {}".format(project["name"], project["id"])
        )

        logger.info("initialise project on disk..")
        kttk.init_entity("project", project["id"])

        logger.info(
            "{entity_type} with id {entity_id} initialised. Done.".format(
                entity_type="project", entity_id=project["id"]
            )
        )
    else:
        is_asset = entity_type == "asset"
        is_task = entity_type == "task"

        if is_asset:
            if not asset_type:
                print_result("no asset type")
                # todo hints for asset_type
                return

        if is_task:
            if not task_step:
                # todo hints for task_step
                print_result("no task step")
                return

        logger.info("initialise {}".format(entity_type))

        current_location = os.getcwd()
        # current_location = r"M:\Projekte\2018\my_awesome_project"
        logger.info("Restore context from location {}..".format(current_location))

        context = kttk.context_from_path(current_location)
        if not context:
            print_result("No context provided for path")
            return

        logger.info("Context is {context}".format(context=context))

        logger.info("create {} in database..".format(entity_type))

        entity_data = {}
        entity_data["code"] = entity_name
        entity_data["project"] = context.project

        if is_asset:
            entity_data["asset_type"] = asset_type

        if is_task:
            entity_data["name"] = entity_name
            entity_data["step"] = task_step
            if not context.entity:
                print_result("No entity provided for task")
                return

            entity_data["entity"] = context.entity

            entity_data["assigned"] = {
                "type": "user",
                "id": "5af33abd6e87ff056014967a",
            }  # todo dont hardcode user id, use kttk.restore_user()

        entity = kt.create(entity_type, entity_data)

        logger.info(
            "created {entity_type} {entity_name} with id {entity_id}.".format(
                entity_type=entity["type"],
                entity_name=entity.get("code")
                if entity.get("code")
                else entity["name"],
                entity_id=entity["id"],
            )
        )

        logger.info("initialise entity on disk..")

        kttk.init_entity(entity_type, entity["id"])

        logger.info(
            "{entity_type} with id {entity_id} initialised. Done.".format(
                entity_type=entity["type"], entity_id=entity["id"]
            )
        )


def find_one(entity_type, entity_id):
    # type: (str, KtrackIdType) -> None
    """
    Finds the given entity in the database and pretty prints it
    :param entity_type: type of the entity
    :param entity_id: id of the entity
    :return: None
    """
    kt = ktrack_api.get_ktrack()

    entity = None
    try:
        entity = kt.find_one(entity_type, entity_id)
    except EntityMissing:
        print_result("Entity type '{}' does not exist".format(entity_type))
        return

    if entity:
        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(entity)
    else:
        print_result(
            'Entity of type "{}" and id "{}" not found..'.format(entity_type, entity_id)
        )


# todo add sort by option
# todo add tests
# todo test link_entity_type and link_entity_id
def show(entity_type, link_entity_type=None, link_entity_id=None):
    # type: (str, str, KtrackIdType) -> None

    # make sure entity type is lowercase
    entity_type = entity_type.lower()

    entities = None

    kt = ktrack_api.get_ktrack()

    try:
        # if we have a link_entity_type and link_entity_id, we use a filter
        if link_entity_type and link_entity_id:
            # make sure link_entity_type is also lowercase
            link_entity_type = link_entity_type.lower()
            entities = kt.find(
                entity_type,
                [["link", "is", {"type": link_entity_type, "id": link_entity_id}]],
            )

        # otherwise we get all entities of this type
        else:
            entities = kt.find(entity_type, [])

    except EntityMissing:
        print_result("Entity type {} does not exist".format(entity_type))
        return

    # make sure we got at least one entits
    got_entities = entities is not None and len(entities) > 0

    if got_entities:
        # generate table

        entities = sorted(entities, key=get_name_or_code)

        # get all dict keys from first entity and sort them
        first_entity = entities[0]
        headers = ["id", get_name_or_code(first_entity), "created_at", "created_by"]

        table = []

        for entity in entities:
            entry = (
                entity["id"],
                get_name_or_code(entity),
                entity["created_at"],
                entity["created_by"],
            )

            table.append(entry)

        print_result(tabulate(table, headers=headers))

    else:
        print_result("No entities of type {} found..".format(entity_type))


def print_context(path=os.getcwd()):
    """
    Prints the context for the fiven path
    :param path: path to print context for, default is current directory
    :return: None
    """
    # todo print context more pretty, for example using a util
    context = kttk.path_cache_manager.context_from_path(path)
    if context:
        print_result(context)
    else:
        print_result("No Context registered for path {}".format(path))


def update(entity_type, entity_id, data):
    # type: (str, KtrackIdType, dict) -> None
    # FIXME not working yet
    print(
        "updating entity of type {} with id {} with data {}".format(
            entity_type, entity_id, data
        )
    )


def task_preset():
    # get context
    path = os.getcwd()

    context = kttk.path_cache_manager.context_from_path(path)

    # make sure path was registered and we have a context
    if not context:
        print_result("No Context registered for path {}".format(path))
        return

    # make sure context has project and entity
    assert context.project and context.entity

    # get task presets for entity
    presets = kttk.get_task_presets(context.entity["type"])

    # now create presets
    kt = ktrack_api.get_ktrack()

    for preset in presets:
        logger.info(
            "Creating task {} of step {}".format(preset["name"], preset["step"])
        )
        task = kt.create(
            "task",
            {
                "project": context.project,
                "entity": context.entity,
                "name": preset["name"],
                "step": preset["step"],
            },
        )
        kttk.init_entity(task["type"], task["id"])


def main():
    # restore user, will create a new one if there is nothing to restore. This way we ensure thing like create have a valid user
    user = kttk.restore_user()

    fire.Fire(
        {
            "create": create,
            "find_one": find_one,
            "show": show,
            "context": print_context,
            "task_preset": task_preset
            # TODO add update
        }
    )


if __name__ == "__main__":
    main()
