import pytest

from kttk.context import Context


@pytest.fixture
def populated_context(ktrack_instance):
    kt = ktrack_instance
    project = kt.create("project", {'name': 'my_project'})
    entity = kt.create("asset", {'code': 'my_entity', 'asset_type': 'prop', 'project': project})
    task = kt.create("task", {'name': 'task', 'step': 'anim', 'entity': entity, 'project': project})
    workfile = kt.create("workfile", {'entity': task, 'name': 'workfile', 'path': 'some_path', 'comment': 'awesome',
                                      'version_number': 1, 'project': project})
    user = kt.create("user", {'name': 'user'})
    return Context(project=project,
                   entity=entity,
                   step='anim',
                   task=task,
                   workfile=workfile,
                   user=user)