import os

import pytest


def has_maya():
    # type: () -> bool
    try:
        import maya.cmds as cmds

        return True
    except:
        pass
    return False


maya_only = pytest.mark.skipif(not has_maya(), reason="requires Maya")
