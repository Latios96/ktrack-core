from kttk.file_manager.file_creation_helper import FileCreationHelper


class CreateNewManager(object):
    """
    Class responsible for the Control Flow for creation of a new scene
    """

    # todo add logging
    def __init__(self, engine, view_callback_provider, context):
        self._engine = engine
        self._view_callback_provider = view_callback_provider
        self._context = context
        self._helper = FileCreationHelper(self._engine)
        self.workfile = None

    ############# CONTROL FLOW ####################

    def do_it(self):
        """
        Main Entry point for create new Action. Will start with check, if a scene is currently open.
        If yes: Will ask to use a template or save the current file as new
        If no: Will create a new file based on template, since no file is open
        :return:
        """
        has_scene_open = self._check_scene_open()

        if has_scene_open:
            self._ask_for_template_use()
        else:
            self._create_from_template()

    def _check_scene_open(self):
        """
        Checks if scene is open in DCC
        :return: True if scene is open, else False
        """
        return self._engine.current_file_path() is not None

    def _ask_for_template_use(self):
        """
        Called when a scene is currently open. Asks user if to use Current scene and save as new or use a template file.
        If Template: Will check for unsaved changes
        If Save Current as new: no check for unsaved changes is needed, we can save file as new file
        """
        use_template = self._view_callback_provider.ask_for_template_use()

        if use_template:
            self._check_unsaved_changes()
        else:
            self._save_current_as_new()

    def _check_unsaved_changes(self):
        """
        Checks for unsaved changes and will ask to save them or discard them
        If no unsaved changes are preset, we can create the file from template
        :return:
        """
        has_unsaved_changes = self._engine.has_unsaved_changes()

        if has_unsaved_changes:
            self._ask_for_save()
        else:
            self._create_from_template()

    def _ask_for_save(self):
        save = self._view_callback_provider.ask_for_save()
        if save:
            self._engine.save()

        self._create_from_template()

    ############# ACTIONS, stuff which does more then if else ####################

    def _create_from_template(self):
        """
        Will open a template file in DCC, so we can save current scene as new file
        """
        template_file = self._helper._get_template_file_path()
        self._engine.open_file_by_path(template_file)
        self._save_current_as_new()

    def _save_current_as_new(self):
        """
        Will save currently opened file to new proper location. Can be some scene or template scene
        :return:
        """
        highest_workfile = self._helper._get_highest_workfile(self._context)

        # create new workfile based on context, use existing workfile with highest version number as base
        if highest_workfile:
            self.workfile = self._helper._create_workfile_from(self._context, highest_workfile)
        else:
            self.workfile = self._helper._create_new_workfile(self._context)

        # save as new created workfile
        # save as will also change engine context
        self._engine.save_as(self.workfile)

        self._update_context()

    def _update_context(self):
        """
        Will do the update for current context in scene
        :return:
        """
        # update file for context
        self._engine.update_file_for_context()
