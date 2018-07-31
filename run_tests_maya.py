import pymel.core as pm
import pytest
import os

pytest.main(['-x', os.path.join(os.getcwd(), 'tests'), '--junitxml=junit_xml_test_core_maya.xml', '-o', 'junit_suite_name=test_core'])
pytest.main(['-x', os.path.join(os.getcwd(), 'tests_maya'), '--junitxml=junit_xml_test_maya.xml', '-o', 'junit_suite_name=test_maya'])