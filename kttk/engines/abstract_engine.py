# TODO engine should be Singleton
from kttk.context import Context

class AbstractEngine(object):
    context = None

    name = "Abstract"  # todo read only

    @property
    def current_workfile(self):
        return self.context.workfile

    def change_file(self, new_file):
        """
        Changes context workfile to new file. Will NOT load the file into the DCC!!!
        :param new_file:
        :return:
        """
        # extract contest from the workfile
        project = new_file['project']
        task = new_file['task']
        step = task['step']
        entity = task['entity']  # entity here means shot / asset...

        self.context = Context(project=project, entity=entity, step=step, task=task, workfile=new_file)

    def current_file_path(self):
        """
        Path of the currently opened file
        :return: the path to the currently opened file, None if no file is opened, for example when DCC was just launched
        """
        pass

    def has_unsaved_changes(self):
        """
        Determines if the app has unsaved changes.
        :return: True if has unsaved changes, False if no unsaved changes
        """
        pass

    def open_file(self, file_to_open):
        """
        Opens given workfile in DCC. Opened file will become current workfile. Will call change file
        :param file_to_open: workfile to open
        """
        self.change_file(file_to_open)

    def save(self):
        """
        Saves current file
        """
        pass

    def save_as(self, file_to_save_to):
        """
        Saves current file to given workfile. Context and current_file will ge changed to given workfile
        :param file_to_save_to: workfile, path field will be used for file location
        :return:
        """
        self.change_file(file_to_save_to)

    def update_file_for_context(self):
        """
        Updates all outputs paths for this file, for example Alembic output pats / render output paths.
        Will also call serialize_context_to_file
        :return:
        """
        pass

    def serialize_context_to_file(self):
        pass

    def deserialize_context_from_file(self):
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

    # todo add method to add / create a widget and parent it to the main window
