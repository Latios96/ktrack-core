class FileManager(object):
    """
    Class responsable for opening, creation and advancing giles
    """

    def __init__(self, context):
        # type: (dict) -> None
        self._context = context
        self._current_workfile = None
        self._engine = None # todo get engine

    def open(self, work_file):
        # type: (dict) -> None
        """
        opens given workfile. Current file will become given workfile
        :param work_file:
        :return:
        """
        self._current_workfile = work_file
        raise NotImplementedError()

    def advance(self, workfile=None, comment=""):
        # type: (dict, str) -> dict
        """
        Advances a workfile. If no workfile is provided, current workfile is used
        Current file will become advanced file
        :param workfile: workfile to advance, if None, current workfile is used
        :param comment: Comment for advanced version
        :return: new created workfile
        """
        if not workfile:
            workfile = self._current_workfile
        raise NotImplementedError()

    def create(self, save_current=False):
        # type: (bool) -> object
        """
        Creates a new file, if save_current: will use currenty opened file, else will use template file
        Current file will become newly created file
        :param save_current:
        :return:
        """
        raise NotImplementedError()
