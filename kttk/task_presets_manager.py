"""
Loads task preset dataPreset data is valid if:
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
"""
import valideer

from kttk.config import config_manager

TASK_PRESETS_YML = 'task_presets.yml'
task_preset_schema = valideer.Mapping(
    key_schema=valideer.String,
    value_schema=valideer.HomogeneousSequence(item_schema=valideer.Object(required={'name': valideer.String,
                                                                                    'step': valideer.String})))

_data_presets = config_manager.load_file(TASK_PRESETS_YML,
                                         lambda data: config_manager.validate_schema(data, task_preset_schema))


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
