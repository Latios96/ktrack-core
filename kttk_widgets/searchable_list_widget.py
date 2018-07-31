from Qt import QtCore, QtGui, QtWidgets

from kttk_widgets.entity_list import EntityListModel


class SearchableListWidget(QtWidgets.QWidget):
    selection_changed = QtCore.Signal(list)

    def __init__(self, source_model, parent=None):
        super(SearchableListWidget, self).__init__(parent)
        self._source_model = source_model
        self._setup_ui()

    def _setup_ui(self):
        self._layout = QtWidgets.QVBoxLayout(self)

        self._search_line = QtWidgets.QLineEdit()
        self._search_line.setPlaceholderText("type to filter..")
        self._layout.addWidget(self._search_line)

        self._view = QtWidgets.QListView()

        self._proxy_model = QtCore.QSortFilterProxyModel(self)
        self._proxy_model.setSortRole(QtCore.Qt.DisplayRole)
        self._proxy_model.setSortCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self._proxy_model.setSourceModel(self._source_model)
        self._proxy_model.setDynamicSortFilter(True)
        self._proxy_model.sort(0, QtCore.Qt.AscendingOrder)  # todo fix sorting in combination with filtering

        self._view.setModel(self._proxy_model)

        self._layout.addWidget(self._view)

        self.setLayout(self._layout)
        self.setFocus()

        # connect signal
        self._search_line.textChanged.connect(lambda text: self._proxy_model.setFilterRegExp(text))

        selection_model = self._view.selectionModel()  # use this two line version, otherwise will crash !!!!
        selection_model.selectionChanged.connect(
            lambda x: self.selection_changed.emit([self._proxy_model.mapToSource(a) for a in x.indexes()]))

    def selected_indexes(self):
        selection_model = self._view.selectionModel()  # use this two line version, otherwise will crash !!!!
        # return selection_model.selectedIndexes()
        return [self._proxy_model.mapToSource(a) for a in selection_model.selectedIndexes()]


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    model = QtCore.QStringListModel()
    model.setStringList(["zaser", "buvz", "azulk", "casdr"])

    widget = SearchableListWidget(model)

    widget.show()
    app.exec_()
