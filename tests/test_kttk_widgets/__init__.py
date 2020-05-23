import os

import pytest


def has_pyside_no_dcc():
    # type: () -> bool
    if os.environ.get("TRAVIS"):
        print("running on travis")
        return False
    else:
        print("not running on travis")
    try:
        import maya.cmds as cmds

        return False
    except:
        pass
    try:
        import nuke

        return False
    except:
        pass
    try:
        import hou

        return False
    except:
        pass
    try:
        import PySide

        return True
    except:
        pass
    try:
        import PySide2

        return True
    except:
        pass

    return False


pyside_only = pytest.mark.skipif(not has_pyside_no_dcc(), reason="requires PySide")
