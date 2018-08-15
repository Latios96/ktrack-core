from kttk import engines
from kttk.context import Context
from kttk.file_manager.advance_manager import AdvanceManager
from kttk.file_manager.create_new_manager import CreateNewManager
from kttk.file_manager.open_manager import OpenManager
from kttk.file_manager.view_callback_mixin import ViewCallbackMixin

# todo make private implementation classes / modules private
class FileManager(object):
    """
    Class responsable for opening, creation and advancing files LOGIC. A View layer is responsable for presentation and
    will invoke methods on the FileManager. In some cases FileManager needs a user choice, for example to save unsaved changes.
    This is done by the view_callback_mixin, which encapsulates the user interaction. Different implementations of view_callback_mixin
    can be useful for different situations, for example GUI usage or automated batch usage.
    """

    def __init__(self, view_callback_mixin):
        # type: (ViewCallbackMixin) -> None
        self._engine = engines.current_engine()
        self._view = view_callback_mixin

    # todo add more documentation on expected behavior
    def open(self, workfile):
        # type: (dict) -> None
        """
        Opens given workfile in the DCC of the current engine. When the user has unsaved changes, he is asked if he wants to save.
        If no unsaved changes are present, the file is opened without asking
        After opening the workfile:
        - the engines context will contain the project/entity/task and the opened workfile
        - the engines current current_workfile will match the given file
        :param workfile: workfile to open
        :return:
        """
        open_manager = OpenManager(self._engine, self._view, None)
        open_manager.do_it(workfile)

    def advance(self):
        """
        Advances a workfile.
        After advancing the current workfile:
        - version number of current workfile is increased by one
        - the engines context will contain the advanced workfile
        - the engines current current_workfile will match the advanced workfile
        - the scene file will be updated for the new context
        Will throw NoFileOpen Exception if no file is currently opened
        :return: new created workfile
        """
        advance_manager = AdvanceManager(self._engine, self._view, None)
        advance_manager.do_it()

    def create(self, context):
        # type: (Context) -> dict
        """
        Creates a new file.
        If a file is currently opened, the user can choose to save the current file as new or use a template file.
        If no scene is currently opened and the scene has no unsaved changes, a template file is used by default todo check this in tests
        After creating a new file
        - the engines context will contain the project/entity/task of given context and the newly created workfile
        - the engines current current_workfile will match the given context and the newly created workfile
        - the scene file will be updated for the given context and the newly created workfile
        :param context: Context to create the workfile in
        :return: newly created workfile
        """
        create_new_manager = CreateNewManager(self._engine, self._view, context)
        create_new_manager.do_it()
        return create_new_manager.workfile
