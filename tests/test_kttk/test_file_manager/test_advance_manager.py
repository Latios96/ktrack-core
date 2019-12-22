import uuid

import mock
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
    create_new_manager._view_callback_provider.ask_for_comment.return_value = (
        False,
        None,
    )

    create_new_manager.do_it()

    create_new_manager._helper.create_workfile_from.assert_not_called()


def test_user_entered_comment(create_new_manager):
    # type: (AdvanceManager) -> None
    workfile = {"type": "workfile", "id": str(uuid.uuid4())}
    full_workfile = {"type": "workfile", "id": str(uuid.uuid4()), "version_number": 0}
    with mock.patch("ktrack_api.ktrack.Ktrack.find_one") as mock_find_one:
        mock_find_one.return_value = full_workfile
        comment = "this is a comment"
        context = Context()
        new_workfile = {"type": "workfile", "id": str(uuid.uuid4())}
        create_new_manager._view_callback_provider.ask_for_comment.return_value = (
            True,
            comment,
        )
        create_new_manager._engine.context = context
        create_new_manager._engine.current_workfile = workfile
        create_new_manager._helper.create_workfile_from.return_value = new_workfile

        create_new_manager.do_it()

        create_new_manager._helper.create_workfile_from.assert_called_with(
            context, full_workfile, comment=comment
        )
        create_new_manager._engine.save_as.assert_called_with(new_workfile)
        create_new_manager._engine.update_file_for_context.assert_called_once()
