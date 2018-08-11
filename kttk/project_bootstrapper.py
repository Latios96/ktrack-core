import os
import shutil

import ktrack_api
import kttk
from ktrack_api.ktrack import KtrackIdType
from kttk import name_sanitizer, task_presets_manager, logger, template_manager

_project_names = [
    'Toy Story',
    "A Bug's Life",
    'Toy Story 2',
    'Monsters, Inc.',
    'Finding Nemo',
    'The Incredibles',
    'Cars',
    'Ratatouille',
    'WALL-E',
    'Toy Story 3',
    'Cars 2',
    'Brave',
    'Monsters University',
    'Inside Out',
    'The Good Dinosaur',
    'Finding Dory',
    'Cars 3',
    'Coco',
    'Incredibles 2',
    'Toy Story 4',
    'Frozen',
    'Iron Man',
    'The Incredible Hulk',
    'Iron Man 2',
    'Thor',
    'Captain America: The First Avenger',
    'Iron Man 3',
    'Thor: The Dark World',
    'The Winter Soldier',
    'Guardians of the Galaxy',
    'Avengers: Age of Ultron',
    'Ant-Man',
    'Captain America: Civil War',
    'Doctor Strange',
    'Guardians of the Galaxy Vol. 2',
    'Spider-Man: Homecoming',
    'Thor: Ragnarok',
    'Black Panther',
    'Avengers: Infinity War',
    'Ant-Man and the Wasp',
    'Captain Marvel',
    'Spider-Man: Far From Hom',
    'Guardians of the Galaxy Vol. 3']

data = {'project_name': 'Finding Dory',
        'asset_names': ['Dory', 'Fluke and Rudder', 'Hank'],
        'shot_names': ['shot010', 'shot020', 'shot030', 'shot040']}


def bootstrap_project():
    # type: () -> dict
    """
    Bootstraps a project. Project can be used for testing or demonstration purposes
    :return: the bootstrapped project
    """
    kt = ktrack_api.get_ktrack()

    # sanitize project name
    project_name = name_sanitizer.sanitize_name(data['project_name'])

    # create project
    project = kt.create("project", {'name': project_name})

    # init project
    kttk.init_entity(project['type'], project['id'])

    entity_types = ['asset', 'shot']

    for entity_type in entity_types:
        entity_presets = task_presets_manager.get_task_presets(entity_type)

        for entity in data['{}_names'.format(entity_type)]:
            # sanitize name
            entity_name = name_sanitizer.sanitize_name(entity)

            # create the entity

            entity_data = {'code': entity_name, 'project': project}

            # make sure each asset has an entity type
            if entity_type == 'asset':
                entity_data['asset_type'] = 'character'

            entity = kt.create(entity_type, entity_data)

            # init asset
            kttk.init_entity(entity['type'], entity['id'])

            # apply task preset
            for preset in entity_presets:
                logger.info("Creating task {} of step {}".format(preset['name'], preset['step']))
                task = kt.create('task', {'project': project, 'entity': entity, 'name': preset['name'],
                                          'step': preset['step']})

                kttk.init_entity(task['type'], task['id'])

    return project


# todo add tests
def remove_bootstrapped_project(project_id):
    # type: (KtrackIdType) -> None
    """
    Removes the bootstrapped project. Removes entites from database, deletes folders and unregisters folders in database
    :return:
    """
    # get all entities
    kt = ktrack_api.get_ktrack()

    entities = []

    # get project
    project = kt.find_one("project", project_id)
    entities.append(project)

    # get shots
    shots = kt.find("shot", [['project', 'is', project]])
    entities.extend(shots)

    # get assets
    assets = kt.find("asset", [['project', 'is', project]])
    entities.extend(assets)

    # get asset tasks
    asset_tasks = []
    for asset in assets:
        asset_tasks.extend(kt.find("task", [['entity', 'is', asset]]))
    entities.extend(asset_tasks)

    # get shot tasks
    shot_tasks = []
    for shot in shots:
        shot_tasks.extend(kt.find("task", [['entity', 'is', shot]]))
    entities.extend(shot_tasks)

    # todo unregister workfiles

    # walk project folder and unregister each path
    project_folder_template = template_manager.get_route_template('project_folder')
    project_root_template = template_manager.get_route_template('project_root')
    project_folder = template_manager.format_template(project_folder_template, {'project_name': project['name'],
                                                                                'project_root': project_root_template})

    logger.info("Unregister paths...")

    for root, dirs, files in os.walk(project_folder):
        path = root

        if kttk.path_cache_manager.unregister_path(path):
            logger.info("Unregistered path {}".format(path))

    # delete all entities
    logger.info("Deleting entities...")
    for entity in entities:
        kt.delete(entity['type'], entity['id'])
        logger.info("Deleted {} with id {}".format(entity['type'], entity['id']))

    # delete project folder and subfolders
    logger.info("Remove project folder {}".format(project_folder))
    shutil.rmtree(project_folder)


if __name__ == '__main__':
    project = bootstrap_project()
    remove_bootstrapped_project(project['id'])
