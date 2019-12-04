C:\Python27\Scripts\virtualenv venv
set PATH=%WORKSPACE%/venv/Scripts/;%PATH%
%WORKSPACE%/venv/Scripts/python setup.py install
%WORKSPACE%/venv/Scripts/pip install -r requirements_ci.txt

echo "activating integration tests..."
set KTRACK_ENABLE_INTEGRATION_TESTS=runTrue

echo running regular tests...
set COVERAGE_FILE=coverage_standart.cov
python run_tests.py

set PYTHONPATH=%PYTHONPATH%;%CD%/venv/Lib;%CD%/venv/Lib/site-packages;

echo running maya tests...
set MAYA_APP_DIR=%TEMP%/ktrack_core_tests
set COVERAGE_FILE=coverage_maya.cov
"C:\Program Files\Autodesk\Maya2017\bin\mayapy" run_tests.py

echo running houdini tests...
set COVERAGE_FILE=coverage_houdini.cov
"C:\Program Files\Side Effects Software\Houdini 16.5.323\bin\hython.exe" run_tests.py

set KTRACK_ENABLE_INTEGRATION_TESTS=
%WORKSPACE%/venv/Scripts/coverage combine coverage_standart.cov coverage_maya.cov coverage_houdini.cov
%WORKSPACE%/venv/Scripts/coverage html