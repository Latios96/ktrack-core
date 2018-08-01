import pytest


@pytest.fixture
def project_dict():
    return {'type': 'project', 'id': '123'}


@pytest.fixture
def shot_dict():
    return {'type': 'shot', 'id': '123'}


@pytest.fixture
def asset_dict():
    return {'type': 'asset', 'id': '123'}


@pytest.fixture
def task_dict():
    return {'type': 'task', 'id': '123'}


@pytest.fixture
def workfile_dict():
    return {'type': 'workfile', 'id': '123', 'path': 'some_path'}


@pytest.fixture
def user_dict():
    return {'type': 'user', 'id': '123'}
