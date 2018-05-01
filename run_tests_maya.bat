set MAYA_APP_DIR=%TEMP%/ktrack_core_tests
set PYTHONPATH=%PYTHONPATH%;%CD%/venv/Lib;%CD%/venv/Lib/site-packages;
echo %PYTHONPATH%
"C:\Program Files\Autodesk\Maya2017\bin\mayapy" -c "import pytest;pytest.main(['-x', '%cd%/tests_maya'])"