from kttk.context import Context
from kttk.engines import AbstractEngine
from kttk.file_manager.file_creation_helper import FileCreationHelper
from kttk.file_manager.view_callback_mixin import ViewCallbackMixin


class AdvanceManager(object):

    _helper = None  # type: FileCreationHelper
    _context = None  # type: Context
    _view_callback_provider = None  # type: ViewCallbackMixin
    _engine = None  # type: AbstractEngine

    def __init__(self, engine, view_callback_provider, context):
        self._engine = engine
        self._view_callback_provider = view_callback_provider
        self._context = context
        self._helper = FileCreationHelper(self._engine)
        self.workfile = None

    def do_it(self):
        user_option, comment = self._view_callback_provider.ask_for_comment()

        if user_option:
            new_workfile = self._helper._create_workfile_from(
                self._engine.context, self._engine.current_workfile, comment=comment
            )

            self._engine.save_as(new_workfile)

            self._engine.update_file_for_context()
