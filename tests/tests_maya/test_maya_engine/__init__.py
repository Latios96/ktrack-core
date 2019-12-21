import os

import pytest


def has_maya():
    # type: () -> bool
    """
    Checks if PySioe or PySide2 is avaible
    :return: True if avaible, False otherwise
    """
    try:
        import maya.cmds as cmds

        return True
    except:
        pass
    return False


maya_only = pytest.mark.skipif(not has_maya(), reason="requires Maya")
