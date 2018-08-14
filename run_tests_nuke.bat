set PYTHONPATH=%PYTHONPATH%;%CD%/venv/Lib;%CD%/venv/Lib/site-packages;
set COVERAGE_FILE=coverage_nuke.cov
"C:\Program Files\Nuke11.1v3\Nuke11.1.exe" -nc -t run_tests.py