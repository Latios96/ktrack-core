import os

import ktrack_api
from ktrack_api.ktrack import KtrackIdType

from kttk import template_manager, path_cache_manager
from kttk.context import Context
from . import logger


def init_entity(entity_type, entity_id):
    # type: (str, KtrackIdType) -> None
    """
    Initialises an entity for production.
    This contains:
    - creating all folders for this entity on disk
    - register all created folders with path_cache_manager in database
    - run setup scripts, example could be USD setup. This is currently not supported
    Instead of lazily creating folders, we create all folders automatically, so we dont have to check if the folders already exist
    :param entity_type: type of entity to initialise, is expected to be a project entity
    :param entity_id: id of entity to initialise
    :return:
    """
    kt = ktrack_api.get_ktrack()

    # get project from entity
    entity = kt.find_one(entity_type, entity_id)
    entity_is_project = entity["type"] == "project"

    if entity_is_project:
        project = entity
    else:
        project = kt.find_one("project", entity["project"]["id"])

    # construct context
    context = Context(project=project, entity=None if entity_is_project else entity)

    # get all folders and files
    file_templates, folder_templates = template_manager.get_file_and_folder_templates(
        entity_type
    )

    # create files and folders
    # construct context dict
    context_dict = context.as_dict()
    context_dict.update(entity)

    all_routes = template_manager.get_all_route_templates()
    context_dict.update(all_routes)

    context_dict["project_root"] = template_manager.get_route_template("project_root")
    context_dict["project_name"] = project["name"]
    context_dict["project_year"] = project["created_at"].year

    logger.info(
        "Creating folders for {} {}..".format(
            entity_type,
            entity.get("name") if entity.get("name") else entity.get("code"),
        )
    )
    # create folders
    for folder_template in folder_templates:
        path = template_manager.format_template(folder_template, context_dict)

        if not os.path.exists(path):
            logger.info("Create folder {}".format(path))
            os.makedirs(path)

        # register folders in database with context
        logger.info("Register path {}".format(path))
        path_cache_manager.register_path(path, context)

    logger.info(
        "Creating files for {} {}..".format(
            entity_type,
            entity.get("name") if entity.get("name") else entity.get("code"),
        )
    )
    # create files
    for file_template in file_templates:
        file_path = template_manager.format_template(
            file_template["path"], context_dict
        )
        content = template_manager.format_template(
            file_template["content"], context_dict
        )

        with open(file_path, "w") as f:
            f.write(content)

        # register the created paths in database
        file_folder = os.path.dirname(file_path)
        path_cache_manager.register_path(file_folder, context)
        logger.info("Register path {}".format(file_folder))

    # register entity folder
    entity_folder_template = template_manager.get_route_template(
        "{}_folder".format(entity_type)
    )
    entity_folder = template_manager.format_template(
        entity_folder_template, context_dict
    )

    if entity_folder != "":
        path_cache_manager.register_path(entity_folder, context)
        logger.info("Register path {}".format(entity_folder))

    # run setup hooks todo implement setup hooks


# todo provide unitiliaze_entity method
