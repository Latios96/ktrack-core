set MAYA_APP_DIR=%TEMP%/ktrack_core_tests
set PYTHONPATH=%PYTHONPATH%;%CD%\venv\Lib;%CD%\venv\Lib\site-packages;
set COVERAGE_FILE=coverage_maya.cov
"C:\Program Files\Autodesk\Maya2017\bin\mayapy" run_tests.py