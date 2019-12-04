from Qt import QtCore, QtGui, QtWidgets


class EntityListModel(QtCore.QAbstractListModel):

    def __init__(self):
        super(EntityListModel, self).__init__()

        self._entities = []

    def rowCount(self, parent):
        return len(self._entities)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            entity = self._entities[index.row()]

            if isinstance(entity, dict):
                name = entity.get("name")
                if name:
                    return name

                code = entity.get("code")
                if code:
                    return code
                return "<no name>"
            return entity

    def set_entities(self, entities):
        # first remove all rows
        self.beginRemoveRows(QtCore.QModelIndex(), 0, len(self._entities) - 1)
        self._entities = []
        self.endRemoveRows()

        # now set new rows
        self.beginInsertRows(QtCore.QModelIndex(), 0, len(entities) - 1)
        self._entities = entities
        self.endInsertRows()
        # todo also store entity in userData Role, so i think its possible to access it through a proxyModel

    def get_entity(self, row):
        return self._entities[row]


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    model = EntityListModel()
    model.set_entities(["zaser", "buvz", "azulk", "casdr"])

    proxy_model = QtCore.QSortFilterProxyModel()
    proxy_model.setSourceModel(model)

    widget = QtWidgets.QListView()
    widget.setModel(proxy_model)

    widget.show()
    app.exec_()
