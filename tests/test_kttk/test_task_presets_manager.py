import pytest
from mock import patch
from typing import Optional, Any
from valideer import ValidationError

from kttk import task_presets_manager


def test_presets_schema_valid():
    # test valid
    data = {"asset": [{"step": "anim", "name": "anim"}]}
    assert task_presets_manager.task_preset_schema.validate(data)


def test_presets_schema_invalid():
    # test not list of presets
    data = {"asset": {"step": "anim", "name": "anim"}}
    with pytest.raises(ValidationError):
        task_presets_manager.task_preset_schema.validate(data)

    # test preset is not dict
    data = {"asset": [[]]}
    with pytest.raises(ValidationError):
        task_presets_manager.task_preset_schema.validate(data)

    # test preset missing step / anim

    data = {"asset": [{"e": "anim", "w": "anim"}]}
    with pytest.raises(ValidationError):
        task_presets_manager.task_preset_schema.validate(data)


def test_get_task_presets():
    yml_data = {
        "shot": [{"step": "anim", "name": "anim"}, {"step": "lsr", "name": "lsr"}]
    }
    with patch.object(task_presets_manager, "_data_presets", yml_data) as mock_yml_data:
        shot_presets = task_presets_manager.get_task_presets("shot")

        assert len(shot_presets) == 2
        preset = shot_presets[0]
        assert isinstance(preset, dict)

        step = preset.get("step")  # type: str
        assert step.islower()

        name = preset.get("name")  # type: str
        assert name.islower()

        # test get None
        with pytest.raises(KeyError):
            presets = task_presets_manager.get_task_presets(None)

        # test get non existing entity
        with pytest.raises(KeyError):
            presets = task_presets_manager.get_task_presets("non_existing_entity")
