import valideer
from typing import Dict, Tuple

from kttk.config import config_manager

TASK_PRESETS_YML = 'task_presets.yml'


def validate_presets(presets_data):
    # type: (Dict) -> Tuple[bool, str]
    """
    Validates given presets_data. Preset data is valid if:
    - its dict with entity types as keys, containing a list of presets
    - each preset has to contain name and step keys
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
    :return: (True, '') if valid, (False, reason) if invalid
    """

    schema = valideer.Mapping(
        key_schema=valideer.String,
        value_schema=valideer.HomogeneousSequence(item_schema=valideer.Object(required={'name': valideer.String,
                                                                                      'step': valideer.String})))
    try:
        schema.validate(presets_data)
        return True, ''
    except valideer.ValidationError as e:
        return False, e.message


_data_presets = config_manager.load_file(TASK_PRESETS_YML, validate_presets)


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
