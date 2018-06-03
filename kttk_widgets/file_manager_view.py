from Qt import QtCore, QtGui, QtWidgets

import ktrack_api
from kttk.context import Context
from kttk.file_manager.file_manager import FileManager
from kttk_widgets.context_widget import ContextWidget
from kttk_widgets.entity_list import EntityListModel
from kttk_widgets.searchable_list_widget import SearchableListWidget

from PySide import QtCore

from kttk_widgets.view_callback_mixin.view_callback_qt_impl import ViewCallbackQtImplementation


class DataRetriver(object):

    def __init__(self):
        self._kt = ktrack_api.get_ktrack()

    def get_my_tasks(self, user):
        return self._kt.find("task", [['assigned', 'is', user]])

    def get_workfiles(self, task):
        return self._kt.find("workfile", [['entity', 'is', task]])


class FileManagerWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FileManagerWidget, self).__init__(parent)
        self._data_retriver = DataRetriver()
        self._view_callback_mixin = ViewCallbackQtImplementation()
        self._file_manager = FileManager(self._view_callback_mixin)
        self._setup_ui()
        self._init()

    def _setup_ui(self):
        task_layout = QtWidgets.QVBoxLayout()
        task_layout.addWidget(QtWidgets.QLabel("<b>My Tasks"))

        self.task_model = EntityListModel()

        self._task_list_view = SearchableListWidget(self.task_model)
        self._task_list_view.selection_changed.connect(lambda indexes: self.task_selection_changed(indexes))
        task_layout.addWidget(self._task_list_view)

        workfile_layout = QtWidgets.QVBoxLayout()
        workfile_layout.addWidget(QtWidgets.QLabel("<b>Workfiles</b>"))

        self.workfile_model = EntityListModel()

        self._workfile_list_view = SearchableListWidget(self.workfile_model)
        # self._workfile_list_view.selection_changed.connect(lambda indexes: self._update_w(indexes))
        workfile_layout.addWidget(self._workfile_list_view)

        # create new, advance, open
        operations_layout = QtWidgets.QHBoxLayout()

        # create_new
        self._btn_create_new = QtWidgets.QPushButton("create new")
        self._btn_create_new.clicked.connect(lambda: self._create())
        self._btn_create_new.setEnabled(False)
        operations_layout.addWidget(self._btn_create_new)

        # advance
        self._btn_advance = QtWidgets.QPushButton("advance")
        operations_layout.addWidget(self._btn_advance)

        # open
        self._btn_open = QtWidgets.QPushButton("open")
        operations_layout.addWidget(self._btn_open)

        self._context_view = ContextWidget(None, self)

        self._layout = QtWidgets.QGridLayout()
        self._layout.addLayout(task_layout, 0, 0)
        self._layout.addLayout(workfile_layout, 0, 1)
        self._layout.addWidget(self._context_view, 1, 0)
        self._layout.addLayout(operations_layout, 1, 1)

        self.setLayout(self._layout)

    def _init(self):
        tasks = self._data_retriver.get_my_tasks({'type': 'user', 'id': '5af33abd6e87ff056014967a'})
        self.task_model.set_entities(tasks)

    def _update_w(self, selected_indexes):
        print self.workfile_model.get_entity(selected_indexes[0].row())['name']

    def task_selection_changed(self, selected_indexes):
        if len(selected_indexes) > 0:
            task = self.task_model.get_entity(selected_indexes[0].row())
            workfiles = self._data_retriver.get_workfiles(task)
            print workfiles
            self.workfile_model.set_entities(workfiles)

            # enable button
            self._btn_create_new.setEnabled(True)

            # self._context_from_task(task)
        else:
            self.workfile_model.set_entities([])
            self._btn_create_new.setEnabled(False)

    def _create(self):
        indexes = self._task_list_view.selected_indexes()

        if len(indexes) > 0:
            # get selected task
            task = self.task_model.get_entity(indexes[0].row())

            # create a context from task, so we can create a new workfile there
            context = self._context_from_task(task)
            self._file_manager.create(context)


    def _context_from_task(self, task):
        context = Context(project=task['project'], entity=task['entity'], task=task, step=task['step'])
        return context



if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = FileManagerWidget()
    widget.show()

    app.exec_()
