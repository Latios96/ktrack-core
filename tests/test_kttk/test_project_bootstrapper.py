import os

from mock import mock, patch

import kttk
from kttk import project_bootstrapper
from tests import integration_test_only

data = {
    "project_name": "Finding Dory",
    "asset_names": ["Dory", "Fluke and Rudder", "Hank"],
    "shot_names": ["shot010", "shot020", "shot030", "shot040"],
}

task_presets = {
    "asset": [{"step": "anim", "name": "anim"}],
    "shot": [{"step": "anim", "name": "anim"}],
}


def test_bootstrap_project(ktrack_instance):
    # mock project data
    with patch.object(kttk.project_bootstrapper, "data", new=data) as mock_data:
        with patch.object(
            kttk.task_presets_manager, "_data_presets", new=task_presets
        ) as mock_task_presets:
            # mock ktrack
            with patch("ktrack_api.get_ktrack") as mock_get_ktrack:
                mock_get_ktrack.return_value = ktrack_instance

                # mock entity init
                with patch("kttk.init_entity") as mock_init_entity:
                    assert project_bootstrapper.bootstrap_project()

                    assert (
                        mock_init_entity.call_count == 15
                    )  # 15: 1 project + 3 assets + 4 shots + 3*3 asset tasks + 3*4 shot tasks


def test_remove_bootstrapped_project(ktrack_instance_patched):
    # setup bootstrapped project
    kt = ktrack_instance_patched

    entities = []
    # create project
    project = kt.create("project", {"name": "Finding_Dory"})

    # create some assets with tasks and workfiles
    for asset_name in data["asset_names"]:
        asset = kt.create(
            "asset",
            {
                "code": asset_name.replace(" ", ""),
                "asset_type": "character",
                "project": project,
            },
        )
        entities.append(asset)

        for task_preset in task_presets["asset"]:
            task = kt.create(
                "task",
                {
                    "project": project,
                    "name": task_preset["name"],
                    "step": task_preset["step"],
                    "entity": asset,
                },
            )
            entities.append(task)

            # create a workfile for task
            workfile = kt.create(
                "workfile", {"project": project, "entity": asset, "path": "123"}
            )
            entities.append(workfile)

    # create some assets with tasks and workfiles
    for shot_name in data["shot_names"]:
        shot = kt.create(
            "shot", {"code": shot_name.replace(" ", ""), "project": project}
        )
        entities.append(shot)

        for task_preset in task_presets["shot"]:
            task = kt.create(
                "task",
                {
                    "project": project,
                    "name": task_preset["name"],
                    "step": task_preset["step"],
                    "entity": shot,
                },
            )
            entities.append(task)

            # create a workfile for task
            workfile = kt.create(
                "workfile", {"project": project, "entity": shot, "path": "123"}
            )
            entities.append(workfile)

    # mock file system access
    with mock.patch("os.walk") as mock_walk:
        mock_walk.return_value = [("", "", "")]

        with mock.patch("shutil.rmtree") as mock_rmtree:
            with mock.patch(
                "kttk.path_cache_manager.unregister_path"
            ) as mock_unregister_path:
                # now remove the project
                project_bootstrapper.remove_bootstrapped_project(project["id"])

                mock_rmtree.assert_called()

                # make sure all entities where deleted

    for entity in entities:
        print(entity["type"])
        assert kt.find_one(entity["type"], entity["id"]) is None


@integration_test_only
def test_project_bootstrapping():
    project, project_data = project_bootstrapper.bootstrap_project()
    year = project["created_at"].year

    assert os.path.isdir("M:/Projekte/{}/Finding_Dory".format(year))
    assert os.path.isdir(
        "M:/Projekte/{}/Finding_Dory/Assets/character/Hank".format(year)
    )

    project_bootstrapper.remove_bootstrapped_project(project["id"])

    assert not os.path.isdir("M:/Projekte/{}/Finding_Dory".format(year))
    assert not os.path.isdir(
        "M:/Projekte/{}/Finding_Dory/Assets/character/Hank".format(year)
    )
