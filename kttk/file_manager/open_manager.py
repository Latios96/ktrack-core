from mock import MagicMock

from kttk.file_manager.file_creation_helper import FileCreationHelper


class OpenManager(object):
    """
    Class responsible for the Control Flow for creation of opening a workfile
    """

    def __init__(self, engine, view_callback_provider, context):
        self._engine = engine
        self._view_callback_provider = view_callback_provider
        self._context = context
        self._helper = FileCreationHelper(self._engine)
        self.workfile = None

    def do_it(self, workfile):
        # check if scene is already open
        if self._engine.current_file_path() == workfile["path"]:
            # ask for reload
            if (
                self._view_callback_provider.ask_for_reload() == True
            ):  # explicit True, can also return "canceled"
                self._open_scene()
            else:
                return

        # check for unsaved changes
        if self._engine.has_unsaved_changes():
            save = self._view_callback_provider.ask_for_save()

            if save == True:  # explicit True, can also return "canceled"
                self._engine.save()
            elif save == "cancel":
                return
        self._open_scene(workfile)

    def _open_scene(self, workfile):
        self._engine.open_file(workfile)
