import pytest
from kttk.context import Context

try:
    from kttk_widgets.context_widget import ContextWidget
except ImportError:
    pass

from tests.test_kttk_widgets import pyside_only


@pyside_only
def test_context_setter(qtbot, populated_context):
    context_widget = ContextWidget(None)
    qtbot.add_widget(context_widget)

    # context_changed should be called when context changes

    # verify with populated_context
    with qtbot.wait_signal(context_widget.context_changed):
        context_widget.context = populated_context

    # verify only emitted on change
    with qtbot.assert_not_emitted(context_widget.context_changed):
        context_widget.context = populated_context

    # verifiy change to None
    with qtbot.wait_signal(context_widget.context_changed):
        context_widget.context = None

        # verify only emitted on change
    with qtbot.assert_not_emitted(context_widget.context_changed):
        context_widget.context = None

    # test to set something different than a context
    with pytest.raises(TypeError):
        context_widget.context = ContextWidget


@pyside_only
def test_render_context_full(qtbot, fully_populated_context):
    context_widget = ContextWidget(None)
    qtbot.add_widget(context_widget)

    # test renders correctly with populated_context
    context_widget.context = fully_populated_context

    assert context_widget._project_name_label.text() == fully_populated_context.project['name']
    assert context_widget._entity_name_label.text() == "{} <i>{}</i>".format(fully_populated_context.entity['code'],
                                                                             fully_populated_context.entity['type'])
    assert context_widget._task_name_label.text() == "{} <i>{}</i>".format(fully_populated_context.task['name'],
                                                                           fully_populated_context.task['step'])
    assert context_widget._workfile_name_label.text() == fully_populated_context.workfile['name']
    assert context_widget._user_name_label.text() == fully_populated_context.user['name']


@pyside_only
def test_render_context_empty(qtbot, fully_populated_context):
    context_widget = ContextWidget(None)
    qtbot.add_widget(context_widget)

    # test renders correctly with empty context
    context_widget.context = Context()
    assert context_widget._project_name_label.text() == "<i>None</i>"
    assert context_widget._entity_name_label.text() == "<i>None</i>"
    assert context_widget._task_name_label.text() == "<i>None</i>"
    assert context_widget._workfile_name_label.text() == "<i>None</i>"
    assert context_widget._user_name_label.text() == "<i>None</i>"

    # test correctly with None context
    context_widget.context = None
    assert context_widget._project_name_label.text() == "<i>None</i>"
    assert context_widget._entity_name_label.text() == "<i>None</i>"
    assert context_widget._task_name_label.text() == "<i>None</i>"
    assert context_widget._workfile_name_label.text() == "<i>None</i>"
    assert context_widget._user_name_label.text() == "<i>None</i>"
