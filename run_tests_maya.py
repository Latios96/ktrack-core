import pymel.core as pm
import os
import sys

# when running in Jenkins, Maya does not like backslashes
venv_path = os.path.join(os.path.dirname(__file__), 'venv', 'Lib', 'site-packages')
venv_path = venv_path.replace("\\", "/")
print "venv_path", venv_path
sys.path.append(venv_path)

import pytest

pytest.main(['-x', os.path.join(os.getcwd(), 'tests'), '--junitxml=junit_xml_test_core_maya.xml', '-o', 'junit_suite_name=test_core'])
pytest.main(['-x', os.path.join(os.getcwd(), 'tests_maya'), '--junitxml=junit_xml_test_maya.xml', '-o', 'junit_suite_name=test_maya'])