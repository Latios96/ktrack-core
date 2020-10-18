import sys
import pytest

MAYA = False
NUKE = False
HOUDINI = False
try:
    import pymel.core as pm
    MAYA = True
except ImportError:
    pass

try:
    import nuke
    NUKE = True
except ImportError:
    pass

try:
    import hou
    HOUDINI = True
except ImportError:
    pass


def get_current_interpreter():
    # type: () -> str
    global MAYA, NUKE
    if MAYA:
        return "maya"
    elif NUKE:
        return "nuke"
    elif HOUDINI:
        return "houdini"
    else:
        return "standalone_python"


if __name__ == "__main__":
    interpreter = get_current_interpreter()
    print("running tests in {}...".format(interpreter))

    pytest.main(pytest.main(sys.argv[1:]))
