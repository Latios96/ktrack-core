from Qt import QtCore, QtGui, QtWidgets
from mock import MagicMock


class FileManagerOperationsWidget(QtWidgets.QWidget):

    def __init__(self, file_manager, parent=None):
        super(FileManagerOperationsWidget, self).__init__(parent)
        self._file_manager = file_manager
        self._published_file_view = MagicMock()
        self._setup_ui()

    def _setup_ui(self):
        # todo add tooltips?
        self._layout = QtWidgets.QHBoxLayout()

        # create_new
        self._btn_create_new = QtWidgets.QPushButton("create new")
        self._btn_create_new.clicked.conntext(lambda: self._file_manager.engine_context)
        self._layout.addWidget(self._btn_create_new)

        # advance
        self._btn_advance = QtWidgets.QPushButton("advance")
        self._layout.addWidget(self._btn_advance)

        # open
        self._btn_open = QtWidgets.QPushButton("open")
        self._btn_open.clicked.connect(lambda: self._file_manager.open(self._published_file_view.selected_file()))
        self._layout.addWidget(self._btn_open)

        self.setLayout(self._layout)


class _OperationsMock(object):

    def __init__(self, view_callback_mixin):
        pass

    @property
    def engine_context(self):
        return MagicMock()

    def open(self, workfile):
        print "open file"

    def advance(self, comment=""):
        print "advance file"

    def create(self, context):
        print "create"


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = FileManagerOperationsWidget(_OperationsMock(None))
    widget.show()

    app.exec_()
