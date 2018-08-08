import os
import pytest

print "running tests in Nuke..."

import coverage

cov = coverage.Coverage(include=['*kttk*', '*ktrack_api*', '*kttk_widgets*'])
cov.start()

pytest.main(['-x', os.path.join(os.getcwd(), 'tests'), '--junitxml=junit_xml_test_nuke.xml', '-o', 'junit_suite_name=test_nuke'])

cov.stop()
cov.save()
cov.xml_report(outfile='coverage_tests_nuke.xml')