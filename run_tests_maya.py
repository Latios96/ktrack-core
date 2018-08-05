import os
import pytest
import pymel.core as pm

print "running tests in Maya..."
pytest.main(['-x', os.path.join(os.getcwd(), 'tests'), '--junitxml=junit_xml_test_maya.xml', '-o', 'junit_suite_name=test_maya'])