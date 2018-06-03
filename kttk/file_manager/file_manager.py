from kttk import engines
from kttk.file_manager.create_new_manager import CreateNewManager


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
        :param work_file: workfile to open
        :param force: if unsaved changes are present and force is True, no UnsavedChangesException is thrown and file is opened.
        :return:
        """

        raise NotImplementedError()

    def advance(self, comment=""):
        # type: (dict, str) -> dict
        """
        Advances a workfile. New workfile will become current workfile, version number will be increased. Workfile will be updated for context.
        Will throw NoFileOpen Exception if no file is currently opened
        :param comment: Comment for advanced version
        :return: new created workfile
        """
        # check if a file is opened, if not,
        # create a new workfile based on current workfile: increase version number, name also changes
        # saveAs with just created workfile
        # update for context
        raise NotImplementedError()

    def create(self, context):
        """
        Creates a new file, if save_current: will use currenty opened file, else will use template file
        Current file will become newly created file. Workfile will also be stored in Context
        :param context: Context to create the workfile in
        :return: newly created workfile
        """
        create_new_manager = CreateNewManager(self._engine, self._view, context)
        create_new_manager.do_it()
        return create_new_manager.workfile
