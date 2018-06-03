import mock
from Qt import QtWidgets

from kttk_widgets.view_callback_mixin.view_callback_qt_impl import ViewCallbackQtImplementation


def test_ask_for_save_save(qtbot):
    """
    Tests if ask for save returns True if Save is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Save
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_save() == True


def test_ask_for_save_discard(qtbot):
    """
    Tests if ask for save returns False if Discard is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Discard
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_save() == False


def test_ask_for_save_cancel(qtbot):
    """
    Tests if ask for save returns 'cancel' if Cancel is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Cancel
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_save() == "cancel"


def test_ask_for_reload_yes(qtbot):
    """
    Tests if ask for save returns True if Save is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Yes
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_reload() == True


def test_ask_for_reload_no(qtbot):
    """
    Tests if ask for save returns False if Discard is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.No
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_reload() == False


def test_ask_for_reload_cancel(qtbot):
    """
    Tests if ask for save returns 'cancel' if Cancel is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Cancel
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_reload() == "cancel"
