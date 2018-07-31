import os

import ktrack_api
from ktrack_api.ktrack import KtrackIdType

from kttk import template_manager, path_cache_manager
from kttk.context import Context
from . import logger


def init_entity(entity_type, entity_id):
    # type: (str, KtrackIdType) -> None
    """
    Initialises an entity for production. Will create folders for entity on disk, will register folders in database,
    will run stup scripts, example could be USD setup
    :param entity_type: type of entity to initialise, is expected to be a project entity
    :param entity_id: id of entity to initialise
    :return:
    """
    kt = ktrack_api.get_ktrack()

    # get project from entity
    entity = kt.find_one(entity_type, entity_id)
    entity_is_project = entity['type'] == 'project'

    if entity_is_project:
        project = entity
    else:
        project = entity['project']

    # construct context
    context = Context(project=project, entity=entity)

    # get all folders and files
    file_templates, folder_templates = template_manager.get_file_and_folder_templates(entity_type)

    # create files and folders
    # construct context dict
    context_dict = context.as_dict()
    context_dict.update(entity)

    all_routes = template_manager.get_all_route_templates()
    context_dict.update(all_routes)

    context_dict['project_root'] = template_manager.get_route_template('project_root')
    context_dict['project_name'] = project['name']

    logger.info("Creating folders for {} {}..".format(entity_type,
                                                      entity.get('name') if entity.get('name') else entity.get('code')))
    # create folders
    for folder_template in folder_templates:
        path = template_manager.format_template(folder_template, context_dict)

        if not os.path.exists(path):
            logger.info("Create folder {}".format(path))
            os.makedirs(path)

        # register folders in database with context
        path_cache_manager.register_path(path, context)
        # todo register also top level path for example for asset

    logger.info("Creating files for {} {}..".format(entity_type,
                                                      entity.get('name') if entity.get('name') else entity.get('code')))
    # create files
    for file_template in file_templates:
        file_path = template_manager.format_template(file_template['path'], context_dict)
        content = template_manager.format_template(file_template['content'], context_dict)

        with open(file_path, "w") as f:
            f.write(content)

        # register the created paths in database
        path_cache_manager.register_path(os.path.dirname(file_path), context)

    # register entity folder
    entity_folder_template = template_manager.get_route_template(
        '{}_folder'.format(entity_type))
    entity_folder = template_manager.format_template(entity_folder_template, context_dict)

    if entity_folder != "":
        path_cache_manager.register_path(entity_folder, context)

    # run setup hooks todo implement setup hooks
