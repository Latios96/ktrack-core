import ktrack_api

from kttk import logger
from kttk.context import Context


class AbstractEngine(object):
    context = (
        None
    )  # todo check if somewhere context reference is changed, make read only from outside -> property

    name = "Abstract"  # has to start with upper letter todo read only
    file_extension = ".dat"  # has to start with .

    @property
    def qt_main_window(self):
        # type: () -> QtWidgets.QMainWindow
        """
        Returns a reference to the qt main window of the application.
        :return: reference to qt main window if avaible, else None
        """
        raise NotImplementedError()

    @property
    def current_workfile(self):
        # type: () -> dict
        """
        The workfile currently opened in the DCC. Matches the serialized context in the file
        :return:
        """
        return self.context.workfile

    def change_file(self, new_file):
        # type: (dict) -> None
        """
        Changes context workfile to new file. Called when open or save_as change the DCC workfile.
        Will NOT load the file into the DCC!!!
        :param new_file: workfile which will be opened in the DCC
        :return:
        """
        # extract contest from the workfile
        # load full workfile
        kt = ktrack_api.get_ktrack()

        new_file = kt.find_one("workfile", new_file["id"])

        project = new_file["project"]

        task = kt.find_one("task", new_file["entity"]["id"])
        step = task["step"]
        entity = task["entity"]  # entity here means shot / asset...

        # todo what to do with user? usermanager.restore_user() can lead to issues in travis ci
        self.context = Context(
            project=project,
            entity=entity,
            step=step,
            task=task,
            workfile=new_file,
            user=None,
        )  # todo add context changed signal / callback

        # Note: cant serialize context here, change_workfile is also used when opening a file
        # update_file_for_context will serialze context for us

    def current_file_path(self):
        # type: () -> str
        """
        Path of the currently opened file
        :return: the path to the currently opened file, None if no file is opened, for example when DCC was just launched
        """
        pass

    def has_unsaved_changes(self):
        # type: () -> bool
        """
        Determines if the app has unsaved changes.
        :return: True if has unsaved changes, False if no unsaved changes
        """
        pass

    def open_file(self, file_to_open):
        # type: (dict) -> None
        """
        Opens given workfile in DCC. Opened file will become current workfile. Will call change file
        :param file_to_open: workfile to open
        """
        logger.info("Opening file {}".format(file_to_open))
        self.change_file(file_to_open)

    def open_file_by_path(self, path):
        # type: (str) -> None
        """
        Opens file path in DCC
        """
        logger.info("Opening file {}".format(path))

    def save(self):
        """
        Saves current file to disk
        """
        pass

    def save_as(self, file_to_save_to):
        # type: (dict) -> None
        """
        Saves current file to given workfile. Context and current_file will ge changed to given workfile
        :param file_to_save_to: workfile, path field will be used for file location
        :return:
        """
        logger.info("Save as to path {}".format(file_to_save_to["path"]))
        self.change_file(file_to_save_to)
        self.update_file_for_context()

    def update_file_for_context(self):
        """
        Updates all outputs paths for this file, for example Alembic output pats / render output paths.
        Will also call serialize_context_to_file
        :return:
        """
        logger.info("Updating file for new context..")
        logger.info("Serialize current context to file..")
        self.serialize_context_to_file()

    def serialize_context_to_file(self):
        """
        Serializes the current context of the engine to the DCC scene file. So everytime the scene file is opened,
        the context can be extracted
        Will NOT serialize the User, because the user can change.
        :return:
        """
        pass

    def deserialize_context_from_file(self):
        """
        Deserialzies context from scene file, will populate the user with the current user field
        :return:
        """
        pass

    ## Ideas, not so important and not implemented at the moment##

    def init_engine(self):
        pass

    def icon_256(self):
        pass

    def host_info(self):
        pass

    def has_ui(self):
        pass
