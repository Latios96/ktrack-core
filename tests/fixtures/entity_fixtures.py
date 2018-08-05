import pytest

# todo provide fully populated dicts
@pytest.fixture
def project_dict():
    return {'type': 'project', 'id': '1','name': 'my_project'}


@pytest.fixture
def shot_dict():
    return {'type': 'shot', 'id': '2','code': 'shot010'}


@pytest.fixture
def asset_dict():
    return {'type': 'asset', 'id': '3','code': 'Groooot'}


@pytest.fixture
def task_dict(shot_dict):
    return {'type': 'task', 'id': '4', 'step': 'anim', 'name': 'anim', 'entity': shot_dict}


@pytest.fixture
def workfile_dict():
    return {'type': 'workfile', 'id': '5', 'path': 'some_path', }


@pytest.fixture
def user_dict():
    return {'type': 'user', 'id': '6'}


