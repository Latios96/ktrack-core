import mock

try:
    from Qt import QtWidgets
    from kttk_widgets.view_callback_mixin.view_callback_qt_impl import ViewCallbackQtImplementation
except ImportError:
    pass

from tests.test_kttk_widgets import pyside_only


@pyside_only
def test_ask_for_save_save(qtbot):
    """
    Tests if ask for save returns True if Save is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Save
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_save() == True


@pyside_only
def test_ask_for_save_discard(qtbot):
    """
    Tests if ask for save returns False if Discard is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Discard
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_save() == False


@pyside_only
def test_ask_for_save_cancel(qtbot):
    """
    Tests if ask for save returns 'cancel' if Cancel is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Cancel
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_save() == "cancel"


@pyside_only
def test_ask_for_reload_yes(qtbot):
    """
    Tests if ask for save returns True if Save is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Yes
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_reload() == True


@pyside_only
def test_ask_for_reload_no(qtbot):
    """
    Tests if ask for save returns False if Discard is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.No
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_reload() == False


@pyside_only
def test_ask_for_reload_cancel(qtbot):
    """
    Tests if ask for save returns 'cancel' if Cancel is clicked
    """
    with mock.patch('Qt.QtWidgets.QMessageBox.exec_') as mock_exec:
        mock_exec.return_value = QtWidgets.QMessageBox.Cancel
        qt_impl = ViewCallbackQtImplementation()

        assert qt_impl.ask_for_reload() == "cancel"


@pyside_only
def test_ask_for_comment_ok(qtbot):
    with mock.patch('Qt.QtWidgets.QInputDialog.getText') as mock_getText:
        mock_getText.return_value = "test", True
        qt_impl = ViewCallbackQtImplementation()

        useroption, comment = qt_impl.ask_for_comment()
        assert useroption == True
        assert comment


@pyside_only
def test_ask_for_comment_cancel(qtbot):
    with mock.patch('Qt.QtWidgets.QInputDialog.getText') as mock_getText:
        mock_getText.return_value = "test", False,
        qt_impl = ViewCallbackQtImplementation()

        useroption, comment = qt_impl.ask_for_comment()
        assert useroption == False
        assert comment
