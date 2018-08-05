from mock import mock

from kttk.context import PopulatedContext


def test_populated_context_full(populated_context, ktrack_instance):
    with mock.patch('ktrack_api.ktrack.Ktrack.find_one') as mock_find_one:
        context = PopulatedContext(project=populated_context.project,
                                   entity=populated_context.entity,
                                   step=populated_context.step,
                                   task=populated_context.task,
                                   workfile=populated_context.workfile,
                                   user=populated_context.user)

        mock_find_one.assert_any_call('project', populated_context.project['id'])
        mock_find_one.assert_any_call(populated_context.entity['type'], populated_context.entity['id'])
        mock_find_one.assert_any_call('task', populated_context.task['id'])
        mock_find_one.assert_any_call('workfile', populated_context.workfile['id'])
        mock_find_one.assert_any_call('user', populated_context.user['id'])


def test_populated_context_with_none(populated_context, ktrack_instance):
    with mock.patch('ktrack_api.ktrack.Ktrack.find_one') as mock_find_one:
        context = PopulatedContext()

        mock_find_one.assert_not_called()
