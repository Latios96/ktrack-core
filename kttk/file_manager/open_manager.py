from kttk.file_manager.file_creation_helper import FileCreationHelper


class OpenManager(object):

    # todo add logging
    def __init__(self, engine, view_callback_provider, context):
        self._engine = engine
        self._view_callback_provider = view_callback_provider
        self._context = context
        self._helper = FileCreationHelper(self._engine)
        self.workfile = None

    def do_it(self):
        # check for unsaved changes
        # if yes and not force: throw UnsavedChangesException
        # if no or force, open file
        pass