from Qt import QtWidgets

from kttk.file_manager.view_callback_mixin import ViewCallbackMixin


class ViewCallbackQtImplementation(ViewCallbackMixin):
    """
    Mixin Interface which needs to be implemented by the UI Layer, because FileManager may needs to ask some stuff during file creation
    """

    def ask_for_template_use(self, parent=None):
        """
        Asks if a template file should be used when creating a new file
        :return: Returns True if template should be used, False if no template should be used or "cancel" if user canceled
        """
        msgBox = QtWidgets.QMessageBox(parent)
        msgBox.setWindowTitle("Use template file?")
        msgBox.setText("Use a templat file or save your current scene as new?")

        use_template_button = msgBox.addButton(
            "Use template", QtWidgets.QMessageBox.AcceptRole
        )
        save_current_button = msgBox.addButton(
            "Save current as new", QtWidgets.QMessageBox.AcceptRole
        )
        cancel_button = msgBox.addButton("Cancel", QtWidgets.QMessageBox.RejectRole)

        ret = msgBox.exec_()

        if msgBox.clickedButton() == use_template_button:
            return True
        elif msgBox.clickedButton() == save_current_button:
            return False
        elif msgBox.clickedButton() == cancel_button:
            return self.CANCEL

    def ask_for_save(self, parent=None):
        """
        Asks if current file should be saved
        :return: Returns True if scene should be saved, False if no save, "cancel" if user canceled
        """
        # we can use plain QMessagebox here
        msgBox = QtWidgets.QMessageBox(parent)
        msgBox.setWindowTitle("Unsaved changes")
        msgBox.setText("The scene has been modified.")
        msgBox.setInformativeText("Do you want to save your changes?")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Save
            | QtWidgets.QMessageBox.Discard
            | QtWidgets.QMessageBox.Cancel
        )
        msgBox.setDefaultButton(QtWidgets.QMessageBox.Save)
        ret = msgBox.exec_()
        if ret == QtWidgets.QMessageBox.Save:
            return True
        elif ret == QtWidgets.QMessageBox.Discard:
            return False
        elif ret == QtWidgets.QMessageBox.Cancel:
            return self.CANCEL

    def ask_for_reload(self):
        """
        Asks if currently opened file should be reloaded
        :return: Returns True if scene should be reloaded, False if no save, "cancel" if user canceled
        """
        # we can use plain QMessagebox here
        msgBox = QtWidgets.QMessageBox(parent=None)
        msgBox.setWindowTitle("File already opened")
        msgBox.setText("This scene is already open")
        msgBox.setInformativeText("Do you want to reload the file?")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Yes
            | QtWidgets.QMessageBox.No
            | QtWidgets.QMessageBox.Cancel
        )
        msgBox.setDefaultButton(QtWidgets.QMessageBox.No)
        ret = msgBox.exec_()
        if ret == QtWidgets.QMessageBox.Yes:
            return True
        elif ret == QtWidgets.QMessageBox.No:
            return False
        elif ret == QtWidgets.QMessageBox.Cancel:
            return self.CANCEL

    def ask_for_comment(self):
        """
        Asks for a comment for file advance.
        :return: (useroption, comment) where useroption is True if user pressed ok, False if user canceled.
        Comment should be None if user canceled, else user comment as string (utf-8)
        """
        comment, useroption = QtWidgets.QInputDialog.getText(
            None, "Comment", "Enter comment for new file"
        )
        return useroption, comment.encode("utf_8", "ignore")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    v = ViewCallbackQtImplementation()
    print(v.ask_for_comment())
    app.exec_()
