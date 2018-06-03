from kttk.file_manager.file_creation_helper import FileCreationHelper


class AdvanceManager(object):

    # todo add logging
    def __init__(self, engine, view_callback_provider, context):
        self._engine = engine
        self._view_callback_provider = view_callback_provider
        self._context = context
        self._helper = FileCreationHelper(self._engine)
        self.workfile = None

    def do_it(self): # todo add tests
        # ask for comment
        user_option, comment = self._view_callback_provider.ask_for_comment()

        if user_option == True:
            # do advance
            # create new workfile based on old
            new_workfile = self._helper._create_workfile_from(self._engine.context, self._engine.current_workfile, comment=comment)

            # save current workfile as new_workfile
            self._engine.save_as(new_workfile)

            # update for new context
            self._engine.update_file_for_context()
        else:
            # user has canceled
            pass

    def _open_scene(self):
        print "open scene"