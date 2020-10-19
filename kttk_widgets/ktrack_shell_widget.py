from logging import StreamHandler

from Qt import QtWidgets
from mongoengine import connect

from kttk import logger, formatter
from kttk.commands.command_runner import CommandRunner
from kttk.commands.command_registry import CommandRegistry


class WriteStream(object):
    def __init__(self, text_edit):
        self._text_edit = text_edit

    def write(self, text):
        self._text_edit.append(str(text))


class TextAreaHandler(StreamHandler):
    def __init__(self, text):
        StreamHandler.__init__(self)
        self._text_edit = text

    def emit(self, record):
        self._text_edit.append(self.format(record))


class KtrackShellWidget(QtWidgets.QWidget):

    def __init__(self):
        super(KtrackShellWidget, self).__init__()
        self._setup_ui()

    def _setup_ui(self):
        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)
        self._input_line = QtWidgets.QLineEdit()
        self._layout.addWidget(self._input_line)
        self._text_edit = QtWidgets.QTextEdit()
        self._layout.addWidget(self._text_edit)
        self._stream = WriteStream(self._text_edit)
        self._input_line.returnPressed.connect(self._return_pressed)

        self._log_handler = TextAreaHandler(self._text_edit)
        self._log_handler.setFormatter(formatter)
        self.resize(600, 200)

    def _return_pressed(self):
        parser = CommandRunner(self._stream, CommandRegistry())
        parser.run(self._input_line.text().split(" "))
        self._input_line.setText("")

    def show(self):
        logger.addHandler(self._log_handler)
        super(KtrackShellWidget, self).show()

    def hide(self):
        logger.removeHandler(self._log_handler)
        super(KtrackShellWidget, self).hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    connect("mongoeengine_test", host="mongodb://localhost:27090/ktrack")

    w = KtrackShellWidget()
    w.show()

    app.exec_()
