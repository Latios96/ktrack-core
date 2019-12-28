import uuid

import mock
import pytest
from mock import MagicMock

from kttk.context import Context
from kttk.file_manager.advance_manager import AdvanceManager


@pytest.fixture
def advance_manager(populated_context):
    manager = AdvanceManager(MagicMock(), MagicMock(), populated_context)
    manager._helper = MagicMock()
    return manager


@pytest.fixture
def advance_manager_user_canceled_comment(populated_context):
    view_callback_provider = MagicMock()
    canceled_comment = (False, None)
    view_callback_provider.ask_for_comment.return_value = canceled_comment
    manager = AdvanceManager(MagicMock(), view_callback_provider, populated_context)
    manager._helper = MagicMock()
    return manager


def test_user_canceled(advance_manager_user_canceled_comment):
    # type: (AdvanceManager) -> None
    advance_manager = advance_manager_user_canceled_comment

    advance_manager.do_it()

    advance_manager._helper.create_workfile_from.assert_not_called()


def test_user_entered_comment(advance_manager):
    # type: (AdvanceManager) -> None
    workfile = {"type": "workfile", "id": str(uuid.uuid4())}
    full_workfile = {"type": "workfile", "id": str(uuid.uuid4()), "version_number": 0}

    with mock.patch("ktrack_api.ktrack.Ktrack.find_one") as mock_find_one:
        mock_find_one.return_value = full_workfile
        comment = "this is a comment"
        context = Context()
        new_workfile = {"type": "workfile", "id": str(uuid.uuid4())}
        advance_manager._view_callback_provider.ask_for_comment.return_value = (
            True,
            comment,
        )
        advance_manager._engine.context = context
        advance_manager._engine.current_workfile = workfile
        advance_manager._helper.create_workfile_from.return_value = new_workfile

        advance_manager.do_it()

        advance_manager._helper.create_workfile_from.assert_called_with(
            context, full_workfile, comment=comment
        )
        advance_manager._engine.save_as.assert_called_with(new_workfile)
        advance_manager._engine.update_file_for_context.assert_called_once()
