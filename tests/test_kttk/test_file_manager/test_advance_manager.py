import uuid

import pytest
from mock import MagicMock

from kttk.context import Context
from kttk.file_manager.advance_manager import AdvanceManager


@pytest.fixture
def create_new_manager(populated_context):
    manager = AdvanceManager(MagicMock(), MagicMock(), populated_context)
    manager._helper = MagicMock()
    return manager


def test_user_canceled(create_new_manager):
    # type: (AdvanceManager) -> None
    create_new_manager._view_callback_provider.ask_for_comment.return_value = (False, None)

    create_new_manager.do_it()

    create_new_manager._helper._create_workfile_from.assert_not_called()


def test_user_entered_comment(create_new_manager):
    # type: (AdvanceManager) -> None
    comment = "this is a comment"
    context = Context()
    workfile = {'type': 'workfile', 'id': str(uuid.uuid4())}
    new_workfile = {'type': 'workfile', 'id': str(uuid.uuid4())}
    create_new_manager._view_callback_provider.ask_for_comment.return_value = (True, comment)
    create_new_manager._engine.context = context
    create_new_manager._engine.current_workfile = workfile
    create_new_manager._helper._create_workfile_from.return_value = new_workfile

    create_new_manager.do_it()

    create_new_manager._helper._create_workfile_from.assert_called_with(context, workfile, comment=comment)
    create_new_manager._engine.save_as.assert_called_with(new_workfile)
    create_new_manager._engine.update_file_for_context.assert_called_once()