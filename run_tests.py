import os
import pytest
import coverage

MAYA = False
NUKE = False
try:
    import pymel.core as pm
    MAYA = True

except:
    pass

try:
    import nuke
    NUKE = True

except:
    pass


def get_current_interpreter():
    global MAYA, NUKE
    if MAYA:
        return 'maya'
    elif NUKE:
        return 'nuke'
    else:
        return 'standalone_python'


if __name__ == '__main__':
    interpreter = get_current_interpreter()
    print "running tests in {}...".format(interpreter)

    cov = coverage.Coverage(include=['*kttk*', '*ktrack_api*', '*kttk_widgets*'])
    cov.start()

    pytest.main(['-x', os.path.join(os.getcwd(), 'tests'), '--junitxml=junit_xml_test_{}.xml'.format(interpreter), '-o',
                 'junit_suite_name=test_{}'.format(interpreter)])

    cov.stop()
    cov.save()
    cov.xml_report(outfile='coverage_tests_{}.xml'.format(interpreter))
