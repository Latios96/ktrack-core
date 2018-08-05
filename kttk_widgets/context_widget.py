from Qt import QtCore, QtGui, QtWidgets

from kttk.context import Context

NONE_TEXT = "<i>None</i>"


class ContextWidget(QtWidgets.QWidget):
    context_changed = QtCore.Signal()

    def __init__(self, context, parent=None):
        super(ContextWidget, self).__init__(parent)
        self._setup_ui()
        self._context = None
        self.context = context

    @property
    def context(self):
        return self._context

    @context.setter
    def context(self, context):
        old_context = self._context
        if context:
            if isinstance(context, Context):
                self._context = context.populate_context()
            else:
                raise TypeError()
        else:
            self._context = None

        if old_context != self._context:
            self.context_changed.emit()

        if self._context:
            self._render_context()
        else:
            self._project_name_label.setText(NONE_TEXT)
            self._entity_name_label.setText(NONE_TEXT)
            self._task_name_label.setText(NONE_TEXT)
            self._workfile_name_label.setText(NONE_TEXT)
            self._user_name_label.setText(NONE_TEXT)

    def _render_context(self):
        # todo create and use central entity nice formatter
        # project
        if self.context.project:
            project_name = self.context.project['name']
            project_text = project_name if project_name else NONE_TEXT
            self._project_name_label.setText(project_text)
        else:
            self._project_name_label.setText(NONE_TEXT)

        # entity
        if self.context.entity:
            entity_code = self.context.entity['code']
            entity_type = self.context.entity['type']
            entity_text = "{} <i>{}</i>".format(entity_code if entity_code else None, entity_type)
            self._entity_name_label.setText(entity_text)
        else:
            self._entity_name_label.setText(NONE_TEXT)

        # task
        if self.context.task:
            task_name = self.context.task['name']
            task_step = self.context.task['step']
            entity_text = "{} <i>{}</i>".format(task_name if task_name else None, task_step if task_step else "None")
            self._task_name_label.setText(entity_text)
        else:
            self._task_name_label.setText(NONE_TEXT)

        # workfile
        if self.context.workfile:
            workfile_name = self.context.workfile['name']
            workfile_text = workfile_name if workfile_name else NONE_TEXT
            self._workfile_name_label.setText(workfile_text)
        else:
            self._workfile_name_label.setText(NONE_TEXT)

        # user
        if self.context.user:
            user_name = self.context.user['name']
            user_text = user_name if user_name else NONE_TEXT
            self._user_name_label.setText(user_text)
        else:
            self._user_name_label.setText(NONE_TEXT)

    def _setup_ui(self):
        self._layout = QtWidgets.QGridLayout(self)

        # project
        self._project_label = QtWidgets.QLabel("Project:")
        self._project_name_label = QtWidgets.QLabel()

        self._layout.addWidget(self._project_label, 0, 0)
        self._layout.addWidget(self._project_name_label, 0, 1)

        # entity
        self._entity_label = QtWidgets.QLabel("Entity:")
        self._entity_name_label = QtWidgets.QLabel("shot010 <i>shot</i>")

        self._layout.addWidget(self._entity_label, 1, 0)
        self._layout.addWidget(self._entity_name_label, 1, 1)

        # task
        self._task_label = QtWidgets.QLabel("Task:")
        self._task_name_label = QtWidgets.QLabel("Anim <i>anim</i>")
        self._task_name_label.setTextFormat(QtCore.Qt.RichText)

        self._layout.addWidget(self._task_label, 2, 0)
        self._layout.addWidget(self._task_name_label, 2, 1)

        # workfile
        self._workfile_label = QtWidgets.QLabel("Workfile:")
        self._workfile_name_label = QtWidgets.QLabel("blabla_v001.mb")

        self._layout.addWidget(self._workfile_label, 3, 0)
        self._layout.addWidget(self._workfile_name_label, 3, 1)

        # user
        self._user_label = QtWidgets.QLabel("User:")
        self._user_name_label = QtWidgets.QLabel("Jan")

        self._layout.addWidget(self._user_label, 4, 0)
        self._layout.addWidget(self._user_name_label, 4, 1)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    context = Context(project={'type': 'project', 'name': None},
                      entity={'type': 'shot', 'code': 'shot010'},
                      task={'type': 'task', 'name': 'Anim', 'step': 'anim'},
                      workfile={'type': 'workfile', 'name': 'shot010_anim_v002.mb'})
    widget = ContextWidget(context)
    widget.show()
    app.exec_()
