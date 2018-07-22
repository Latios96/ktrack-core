import pytest

from kttk.context import Context, InvalidEntityException


def test_reation(populated_context):
    # type: (Context) -> None
    assert populated_context.project['name'] == 'my_project'
    assert populated_context.entity['code'] == 'my_entity'
    assert populated_context.step == 'anim'
    assert populated_context.task['name'] == 'task'
    assert populated_context.workfile['name'] == 'workfile'
    assert populated_context.user['name'] == 'user'


def test_context_as_dict(populated_context):
    # type: (Context) -> None

    context_dict = populated_context.as_dict()

    assert context_dict['project'] == populated_context.project
    assert context_dict['entity'] == populated_context.entity
    assert context_dict['step'] == populated_context.step
    assert context_dict['task'] == populated_context.task
    assert context_dict['workfile'] == populated_context.workfile
    assert context_dict['user'] == populated_context.user


def test_context_from_dict():
    context_dict = {}
    context_dict['project'] = {'type': 'project', 'id': 123}
    context_dict['entity'] = {'type': 'shot', 'code': 'my_entity', 'id': 123}
    context_dict['step'] = 'step'
    context_dict['task'] = {'type': 'task', 'id': 123}
    context_dict['workfile'] = {'type': 'workfile', 'id': 123}
    context_dict['user'] = {'type': 'user', 'id': 123}

    context = Context.from_dict(context_dict)

    assert context.project == {'type': 'project', 'id': 123}
    assert context.entity == {'type': 'shot', 'code': 'my_entity', 'id': 123}
    assert context.step == 'step'
    assert context.task == {'type': 'task', 'id': 123}
    assert context.workfile == {'type': 'workfile', 'id': 123}
    assert context.user == {'type': 'user', 'id': 123}


def test_serialize_deserialize(populated_context):
    # type: (Context) -> None

    context_serialized = populated_context.serialize()

    context = Context.deserialize(context_serialized)

    assert context.project == populated_context.project
    assert context.entity == populated_context.entity
    assert context.step == populated_context.step
    assert context.task == populated_context.task
    assert context.workfile == populated_context.workfile
    assert context.user == populated_context.user


def test_repesentation(populated_context):
    # type: (Context) -> None

    representation = populated_context.__repr__()


def test_get_avaible_tokens(populated_context):
    # type: (Context) -> None
    tokens = populated_context.get_avaible_tokens()

    assert tokens['project_name'] == 'my_project'
    assert tokens['code'] == 'my_entity'
    assert tokens['asset_type'] == 'prop'
    assert tokens['step'] == 'anim'
    assert tokens['task_name'] == 'task'
    assert tokens['user_name'] == 'user'
    assert tokens['version'] == 'v001'


def test_validate_entity_dict():
    context = Context()
    # test None
    context._validate_entity_dict(None)

    # test valid dict
    context._validate_entity_dict({'type': 'project', 'id': '123'})

    # test missing id
    with pytest.raises(InvalidEntityException):
        context._validate_entity_dict({'type': 'project'})

    # test missing type
    with pytest.raises(InvalidEntityException):
        context._validate_entity_dict({'id': '123'})

    # test missing type and id
    with pytest.raises(InvalidEntityException):
        context._validate_entity_dict({})


def test_context_immutable():
    """
    Tests that Context can not be changed after construction
    :return:
    """
    context = Context()

    # test project immutable
    with pytest.raises(AttributeError):
        context.project = {'type': 'project', 'id': 123}

    # test entity immutable
    with pytest.raises(AttributeError):
        context.entity = {'type': 'project', 'id': 123}

    # test step immutable
    with pytest.raises(AttributeError):
        context.project = {'type': 'project', 'id': 123}

    # test task immutable
    with pytest.raises(AttributeError):
        context.task = {'type': 'project', 'id': 123}

    # test workfile immutable
    with pytest.raises(AttributeError):
        context.workfile = {'type': 'project', 'id': 123}

    # test user immutable
    with pytest.raises(AttributeError):
        context.user = {'type': 'project', 'id': 123}


def test_copy_context(populated_context):
    # test project
    new_context = populated_context.copy_context(project={'type': 'project', 'id': 123})
    assert new_context.project == {'type': 'project', 'id': 123}
    assert new_context.entity == populated_context.entity
    assert new_context.step == populated_context.step
    assert new_context.task == populated_context.task
    assert new_context.workfile == populated_context.workfile
    assert new_context.user == populated_context.user

    # test entity
    new_context = populated_context.copy_context(entity={'type': 'project', 'id': 123})
    assert new_context.project == populated_context.project
    assert new_context.entity == {'type': 'project', 'id': 123}
    assert new_context.step == populated_context.step
    assert new_context.task == populated_context.task
    assert new_context.workfile == populated_context.workfile
    assert new_context.user == populated_context.user

    # test step
    new_context = populated_context.copy_context(step="test")
    assert new_context.project == populated_context.project
    assert new_context.entity == populated_context.entity
    assert new_context.step == "test"
    assert new_context.task == populated_context.task
    assert new_context.workfile == populated_context.workfile
    assert new_context.user == populated_context.user

    # test task
    new_context = populated_context.copy_context(task={'type': 'project', 'id': 123})
    assert new_context.project == populated_context.project
    assert new_context.entity == populated_context.entity
    assert new_context.step == populated_context.step
    assert new_context.task == {'type': 'project', 'id': 123}
    assert new_context.workfile == populated_context.workfile
    assert new_context.user == populated_context.user

    # test workfile
    new_context = populated_context.copy_context(workfile={'type': 'project', 'id': 123})
    assert new_context.project == populated_context.project
    assert new_context.entity == populated_context.entity
    assert new_context.step == populated_context.step
    assert new_context.task == populated_context.task
    assert new_context.workfile == {'type': 'project', 'id': 123}
    assert new_context.user == populated_context.user

    # test user
    new_context = populated_context.copy_context(user={'type': 'project', 'id': 123})
    assert new_context.project == populated_context.project
    assert new_context.entity == populated_context.entity
    assert new_context.step == populated_context.step
    assert new_context.task == populated_context.task
    assert new_context.workfile == populated_context.workfile
    assert new_context.user == {'type': 'project', 'id': 123}


def test_entity_dicts_equal():
    context = Context()
    # both None, match
    assert context._entity_dicts_equal(None, None)

    # one None
    assert not context._entity_dicts_equal(None, {})
    assert not context._entity_dicts_equal({}, None)

    # both are equal, id and type match
    assert context._entity_dicts_equal({'type': 'project', 'id': '123'}, {'type': 'project', 'id': '123'})

    # not equal because of id
    assert not context._entity_dicts_equal({'type': 'project', 'id': '13'}, {'type': 'project', 'id': '123'})

    # not equal because of type
    assert not context._entity_dicts_equal({'type': 'projeect', 'id': '123'}, {'type': 'project', 'id': '123'})

    # not equal because of id and type
    assert not context._entity_dicts_equal({'type': 'projeect', 'id': '13'}, {'type': 'project', 'id': '123'})


def test_context__equal__(populated_context):
    context_left = Context()
    context_right = Context()

    # test empty context
    assert context_left == context_right

    # test matching populated context
    assert populated_context == populated_context

    # test not matching entity
    assert not populated_context == populated_context.copy_context(entity={'type': 'project', 'id': 123})

    # test not matching step
    assert not populated_context == populated_context.copy_context(step="test")

    # test not matching task
    assert not populated_context == populated_context.copy_context(task={'type': 'project', 'id': 123})

    # test not matching workfile
    assert not populated_context == populated_context.copy_context(workfile={'type': 'project', 'id': 123})

    # test not matching user
    assert not populated_context == populated_context.copy_context(user={'type': 'project', 'id': 123})

def test_context__ne__(populated_context):
    context_left = Context()
    context_right = Context()

    # test empty context
    assert not context_left != context_right

    # test not matching entity
    assert populated_context != populated_context.copy_context(entity={'type': 'project', 'id': 123})

    # test not matching step
    assert populated_context != populated_context.copy_context(step="test")

    # test not matching task
    assert populated_context != populated_context.copy_context(task={'type': 'project', 'id': 123})

    # test not matching workfile
    assert populated_context != populated_context.copy_context(workfile={'type': 'project', 'id': 123})

    # test not matching user
    assert populated_context != populated_context.copy_context(user={'type': 'project', 'id': 123})


