echo "activating integration tests..."
set KTRACK_ENABLE_INTEGRATION_TESTS=runTrue
call run_standart_tests.bat
echo running tests in maya...
call run_tests_maya.bat
echo running tests in nuke...
call run_tests_nuke.bat
echo running tests in houdini...
call run_tests_houdini.bat

set KTRACK_ENABLE_INTEGRATION_TESTS=
coverage combine coverage_standart.cov coverage_maya.cov coverage_nuke.cov coverage_houdini.cov
coverage html