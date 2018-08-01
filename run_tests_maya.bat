call venv/scripts/activate
set MAYA_APP_DIR=%TEMP%/ktrack_core_tests
set PYTHONPATH=%PYTHONPATH%;%CD%\venv\Lib;%CD%\venv\Lib\site-packages;

"C:\Program Files\Autodesk\Maya2017\bin\mayapy" run_tests_maya.py