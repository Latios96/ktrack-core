import os
import yaml

from kttk.template_manager import get_template_dir

TASK_PRESETS_YML = 'task_presets.yml'

yml_file_folders = os.path.join(get_template_dir(), TASK_PRESETS_YML)


def validate_presets(presets_data):
    # type: (dict) -> bool
    """
    Validates given presets_data. Preset data is valid if:
    - its dict with entity types as keys, containing a list of presets
    - each preset has to contain name and step keys and must not contain more keys.
    example:
    {
        'asset': [
            {
                'step': 'anim',
                'name': 'anim',
            }
        ]
    }
    :param presets_data:
    :return:
    """
    # check its not None
    assert presets_data is not None

    # check its a dict
    assert isinstance(presets_data, dict)

    # check this dict is not empty
    assert len(presets_data.keys()) > 0

    # check dict data
    for entity_type, task_presets in presets_data.iteritems():
        # make sure entity type is str or unicode
        assert isinstance(entity_type, str) or isinstance(entity_type, unicode)

        # make sure task_presets is a list
        assert isinstance(task_presets, list)

        # check presets
        for preset in task_presets:
            # make sure preset is a list
            assert isinstance(preset, dict)

            # make sure preset is valid
            assert len(preset.keys()) == 2

            step = preset.get('step')
            name = preset.get('name')

            assert step
            assert name

            assert isinstance(step, str) or isinstance(step, unicode)
            assert isinstance(name, str) or isinstance(name, unicode)

    return True

with open(yml_file_folders) as file_descriptor:
    _data_presets = yaml.load(file_descriptor)
validate_presets(_data_presets)


def get_task_presets(entity_type):
    # type: (str) -> list[dict]
    """
    Returns list of all task templates for given type. Task preset example, everything will be lowercase
    {
        'step': 'anim',
        'name': 'anim'
    }
    :param entity_type: type to get all task templates for
    :return:
    """
    raw_preset = _data_presets[entity_type]
    return [
                {
                    'step': preset['step'].lower(),
                    'name': preset['name'].lower(),
                }
                for preset in raw_preset
            ]