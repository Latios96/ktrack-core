class ViewCallbackMixin(object):
    """
    Mixin Interface which needs to be implemented by the UI Layer, because FileManager may needs to ask some stuff during file creation
    """
    def ask_for_template_use(self):
        raise NotImplementedError()

    def ask_for_save(self):
        raise NotImplementedError()