import mock
from mock import MagicMock

from kttk.task_preset_applicator import TaskPresetApplicator


@mock.patch("kttk.task_preset_applicator.kttk.get_task_presets")
def test_apply_task_presets(mock_get_task_presets):
    mock_get_task_presets.return_value = [
        {"name": "test_name1", "step": "test_step1"},
        {"name": "test_name2", "step": "test_step2"},
    ]
    task_repository = MagicMock()
    init_entity = MagicMock()
    task_preset_applicator = TaskPresetApplicator(task_repository, init_entity)

    task_preset_applicator.apply("asset", "123", "465")

    task_repository.save.assert_called()
    init_entity.assert_called()
