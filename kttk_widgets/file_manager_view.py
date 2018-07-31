from Qt import QtCore, QtGui, QtWidgets

import ktrack_api
import kttk
from kttk.context import Context
from kttk.file_manager.file_manager import FileManager
from kttk_widgets.context_widget import ContextWidget
from kttk_widgets.entity_list import EntityListModel
from kttk_widgets.searchable_list_widget import SearchableListWidget

from kttk_widgets.view_callback_mixin.view_callback_qt_impl import ViewCallbackQtImplementation


# todo add tests
class DataRetriver(object):

    def __init__(self):
        self._kt = ktrack_api.get_ktrack()

    def get_user(self):
        user_information = kttk.restore_user()
        return self._kt.find_one("user", user_information['id'])

    def get_my_tasks(self, user):
        tasks = self._kt.find("task", [['assigned', 'is', user]])
        return tasks

    def get_workfiles(self, task):
        return self._kt.find("workfile", [['entity', 'is', task]])

    def project_from_project_entity(self, task):
        return self._kt.find("project", [['id', 'is', task['project']['id']]])[0]  # todo use find_one

    def entity_from_task(self, task):
        return self._kt.find(str(task['entity']['type']), [['id', 'is', task['entity']['id']]])[0]  # todo use find_one

    def entity_from_workfile(self, workfile):
        return self._kt.find_one(str(workfile['entity']['type']), workfile['entity']['id'])


class FileManagerWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(FileManagerWidget, self).__init__(parent)
        self._data_retriver = DataRetriver()
        self._view_callback_mixin = ViewCallbackQtImplementation()
        self._file_manager = FileManager(self._view_callback_mixin)
        self._setup_ui()
        self._init()

    def _setup_ui(self):
        self.setObjectName("FileManagerWidget")
        self.setWindowTitle("Ktrack File Manager")

        # Window type
        self.setWindowFlags(QtCore.Qt.Window)

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
        self._workfile_list_view.selection_changed.connect(lambda indexes: self.workfile_selection_changed(indexes))
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
        self._btn_advance.clicked.connect(lambda: self._advance())
        operations_layout.addWidget(self._btn_advance)

        # open
        self._btn_open = QtWidgets.QPushButton("open")
        self._btn_open.setEnabled(False)
        self._btn_open.clicked.connect(lambda: self._open())
        operations_layout.addWidget(self._btn_open)

        self._context_view = ContextWidget(None, self)

        self._layout = QtWidgets.QGridLayout()
        self._layout.addLayout(task_layout, 0, 0)
        self._layout.addLayout(workfile_layout, 0, 1)
        self._layout.addWidget(self._context_view, 1, 0)
        self._layout.addLayout(operations_layout, 1, 1)

        self.setLayout(self._layout)

    def _init(self):
        tasks = self._data_retriver.get_my_tasks(
            {'type': 'user', 'id': '5af33abd6e87ff056014967a'})  # todo dont hardcode user id
        self.task_model.set_entities(tasks)

    def _update_w(self, selected_indexes):
        print self.workfile_model.get_entity(selected_indexes[0].row())['name']

    def task_selection_changed(self, selected_indexes):
        if len(selected_indexes) > 0:
            task = self.task_model.get_entity(selected_indexes[0].row())

            workfiles = self._data_retriver.get_workfiles(task)

            self.workfile_model.set_entities(workfiles)

            # enable button
            self._btn_create_new.setEnabled(True)

            context = self._context_from_task(task)
            self._context_view.context = context

        else:
            self.workfile_model.set_entities([])
            self._btn_create_new.setEnabled(False)

    def workfile_selection_changed(self, selected_indexes):
        if len(selected_indexes) > 0:
            # enable open button
            self._btn_open.setEnabled(True)
            workfile = self.workfile_model.get_entity(selected_indexes[0].row())

            context = self._context_from_workfile(workfile)
        else:
            # disable open button
            self._btn_open.setEnabled(False)

            # remove workfile from context
            context = self._context_view.context.copy_context(workfile=None)

        self._context_view.context = context

    def _create(self):
        indexes = self._task_list_view.selected_indexes()

        if len(indexes) > 0:
            # get selected task
            task = self.task_model.get_entity(indexes[0].row())

            # create a context from task, so we can create a new workfile there
            context = self._context_from_task(task)
            self._file_manager.create(context)

            # update published files
            workfiles = self._data_retriver.get_workfiles(task)
            self.workfile_model.set_entities(workfiles)

    def _open(self):
        workfile_index = self._workfile_list_view.selected_indexes()[0]
        workfile = self.workfile_model.get_entity(workfile_index.row())

        self._file_manager.open(workfile)

    def _advance(self):
        self._file_manager.advance()

        # update published files
        task = self.task_model.get_entity(self._task_list_view.selected_indexes()[0].row())
        workfiles = self._data_retriver.get_workfiles(task)
        self.workfile_model.set_entities(workfiles)

    def _context_from_task(self, task):  # todo add tests
        context = Context(project=self._data_retriver.project_from_project_entity(task),
                          entity=self._data_retriver.entity_from_task(task),
                          task=task,
                          step=task['step'],
                          user=self._data_retriver.get_user())

        return context

    def _context_from_workfile(self, workfile):
        context = self._context_view.context.copy_context(workfile=workfile)
        return context


if __name__ == '__main__':
    app = QtWidgets.QApplication([])

    widget = FileManagerWidget()
    widget.show()

    app.exec_()
