import os
import pytest
import pymel.core as pm

print "running tests in Maya..."

import coverage

cov = coverage.Coverage(include=['*kttk*', '*ktrack_api*', '*kttk_widgets*'])
cov.start()

pytest.main(['-x', os.path.join(os.getcwd(), 'tests'), '--junitxml=junit_xml_test_maya.xml', '-o', 'junit_suite_name=test_maya'])

cov.stop()
cov.save()
cov.xml_report(outfile='coverage_tests_maya.xml')