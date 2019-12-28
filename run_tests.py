import os
import mongomock
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

    args = [
        "-x",
        os.path.join(os.getcwd(), "tests"),
        "--junitxml=junit_xml_test_{}.xml".format(interpreter),
        "-o",
        "junit_suite_name=test_{}".format(interpreter),
    ]

    # disable pytest-qt for houdini because of a requirements mismatch
    # for six, both need six>=1.10.0 and houdini has six 1.9.0
    if HOUDINI:
        args.extend(["-p", "no:pytest-qt", "-p", "no:pytest_cov"])

    pytest.main(args)
