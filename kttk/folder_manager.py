import os

import ktrack_api
from kttk import template_manager
from kttk.context import Context


def init_entity(entity_type, entity_id):
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

    # create folders
    for folder_template in folder_templates:
        path = template_manager.format_template(folder_template, context_dict)

        if not os.path.exists(path):
            os.makedirs(path)

        # register folders in database with context
        path_entry_data = {}
        path_entry_data['path'] = path
        path_entry_data['context'] = context.as_dict()

        kt.create('path_entry', path_entry_data)

    for file_template in file_templates:
        file_path = template_manager.format_template(file_template['path'], context_dict)
        content = template_manager.format_template(file_template['content'], context_dict)

        with open(file_path, "w") as f:
            f.write(content)

        path_entry_data = {}
        path_entry_data['path'] = file_path
        path_entry_data['context'] = context.as_dict()

        kt.create('path_entry', path_entry_data) # todo register path in extra method, make path nice formatted so it only contains / and no \

    # register entity folder
    project_folder_template = template_manager.get_route_template(
        '{}_folder'.format(entity_type))  # todo catch when route does not exist and display good error message
    project_folder = template_manager.format_template(project_folder_template, context_dict)

    path_entry_data = {}
    path_entry_data['path'] = project_folder
    path_entry_data['context'] = context.as_dict()

    kt.create('path_entry', path_entry_data)

    # run setup hooks todo implement setup hooks
