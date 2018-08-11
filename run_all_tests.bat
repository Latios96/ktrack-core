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