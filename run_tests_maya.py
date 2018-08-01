import os
import pytest
import pymel.core as pm

print "running core tests in Maya..."
pytest.main(['-x', os.path.join(os.getcwd(), 'tests'), '--junitxml=junit_xml_test_core_maya.xml', '-o', 'junit_suite_name=test_core'])
print "running Maya tests in Maya..."
pytest.main(['-x', os.path.join(os.getcwd(), 'tests_maya'), '--junitxml=junit_xml_test_maya.xml', '-o', 'junit_suite_name=test_maya'])