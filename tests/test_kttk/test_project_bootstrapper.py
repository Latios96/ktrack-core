from mock import mock, patch

import kttk
from kttk import project_bootstrapper


def test_project_bootstrapper(ktrack_instance):
    data = {'project_name': 'Finding Dory',
                                'asset_names': ['Dory', 'Fluke and Rudder', 'Hank'],
                                'shot_names': ['shot010', 'shot020', 'shot030', 'shot040']}

    task_presets ={
        'asset': [
            {
                'step': 'anim',
                'name': 'anim',
            }
            ],
        'shot': [
            {
                'step': 'anim',
                'name': 'anim',
            }
        ]
    }

    # mock project data
    with patch.object(kttk.project_bootstrapper, 'data', new=data)as mock_data:

        with patch.object(kttk.task_presets_manager, '_data_presets', new=task_presets) as mock_task_presets:
            # mock ktrack
            with patch('ktrack_api.get_ktrack') as mock_get_ktrack:
                mock_get_ktrack.return_value = ktrack_instance

                # mock entity init
                with patch('kttk.init_entity') as mock_init_entity:

                    assert project_bootstrapper.bootstrap_project()

                    assert mock_init_entity.call_count == 15 # 15: 1 project + 3 assets + 4 shots + 3*3 asset tasks + 3*4 shot tasks


