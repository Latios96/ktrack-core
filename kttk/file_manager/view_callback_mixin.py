class ViewCallbackMixin(object):
    """
    Mixin Interface which needs to be implemented by the UI Layer, because FileManager may needs to ask some stuff during file creation
    """
    CANCEL = "cancel"
    def ask_for_template_use(self):
        """
        Asks if a template file should be used when creating a new file
        :return: Returns True if template should be used, False if no template should be used or "cancel" if user canceled
        """
        raise NotImplementedError()

    def ask_for_save(self):
        """
        Asks if current file should be saved
        :return: Returns True if scene should be saved, False if no save, "cancel" if user canceled
        """
        raise NotImplementedError()

    def ask_for_reload(self):
        """
        Asks if currently opened file should be reloaded
        :return: Returns True if scene should be reloaded, False if no save, "cancel" if user canceled
        """
        raise NotImplementedError()

    def ask_for_comment(self):
        """
        Asks for a comment for file advance.
        :return: (useroption, comment) where useroption is True if user pressed ok, False if user canceled.
        Comment should be None if user canceled, else user comment as string (utf-8)
        """