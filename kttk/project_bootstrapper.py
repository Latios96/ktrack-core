import ktrack_api
import kttk
from kttk import name_sanitizer, task_presets_manager, logger

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
    """
    Bootstraps a project for testing purposes
    :return:
    """
    kt = ktrack_api.get_ktrack()

    # sanitize project name
    project_name = name_sanitizer.sanitize_name(data['project_name'])

    # create project
    project = kt.create("project", {'name': project_name})

    # init project
    kttk.init_entity(project['type'], project['id'])

    # assets
    asset_presets = task_presets_manager.get_task_presets('asset')

    for asset in data['asset_names']:
        # sanitize name
        asset_name = name_sanitizer.sanitize_name(asset)

        # create the asset
        asset = kt.create("asset", {'code': asset_name, 'project': project})

        # init asset
        kttk.init_entity(asset['type'], asset['id'])

        # apply task preset
        for preset in asset_presets:
            logger.info("Creating task {} of step {}".format(preset['name'], preset['type']))
            task = kt.create('task', {'project': project, 'entity': asset, 'name': preset['name'],
                                      'step': preset['step']})

            kttk.init_entity(task['type'], task['id'])

    # shots:
    # sanitize names
    # create the shots
    # apply task preset
