import pytest


def has_pyside():
    # type: () -> bool
    """
    Checks if PySioe or PySide2 is avaible
    :return: True if avaible, False otherwise
    """
    try:
        import PySide
        return True
    except:
        print "no PySide"
    try:
        import PySide2
        return True
    except:
        print "no PySide2"
    return False


pyside_only = pytest.mark.skipif(not has_pyside(), reason="requires PySide")
