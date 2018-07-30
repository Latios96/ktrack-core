from kttk import engines
from kttk.context import Context
from kttk.file_manager.advance_manager import AdvanceManager
from kttk.file_manager.create_new_manager import CreateNewManager
from kttk.file_manager.open_manager import OpenManager


class FileManager(object):
    """
    Class responsable for opening, creation and advancing files LOGIC. A View layer is responsable for presentation and
    will incoke methods on the FileManager. If FileManager doesnt know what to do, for example is a file is curently opened,
    it will throw an Exception. View Layer has to catch the Exception and handle it. Methods can be invoked with a mode parameter,
    this will tell the FileManager how to handle the Exception cases
    """

    def __init__(self, view_callback_mixin):
        self._engine = engines.current_engine()
        self._view = view_callback_mixin

    def open(self, workfile):
        # type: (dict) -> None
        """
        opens given workfile. Current file will become given workfile
        :param workfile: workfile to open
        :return:
        """
        open_manager = OpenManager(self._engine, self._view, None)
        open_manager.do_it(workfile)

    def advance(self):
        """
        Advances a workfile. New workfile will become current workfile, version number will be increased. Workfile will be updated for context.
        Will throw NoFileOpen Exception if no file is currently opened
        :return: new created workfile
        """
        advance_manager = AdvanceManager(self._engine, self._view, None)
        advance_manager.do_it()

    def create(self, context):
        # type: (Context) -> dict
        """
        Creates a new file, if save_current: will use currenty opened file, else will use template file
        Current file will become newly created file. Workfile will also be stored in Context
        :param context: Context to create the workfile in
        :return: newly created workfile
        """
        create_new_manager = CreateNewManager(self._engine, self._view, context)
        create_new_manager.do_it()
        return create_new_manager.workfile
