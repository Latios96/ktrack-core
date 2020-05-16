setlocal
SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

SET PYTHON_37_PYTHON_EXECUTABLE="%ROOT_FOLDER%\python-envs\py37\interpreter\python.exe"

SET COMBINED_REQUIREMENTS="%~dp0temp\requirements-combined.txt"
type "%ROOT_FOLDER%\requirements.txt" > "%COMBINED_REQUIREMENTS%"
echo. >> "%COMBINED_REQUIREMENTS%"
type "%ROOT_FOLDER%\requirements-dev.txt" >> "%COMBINED_REQUIREMENTS%"

set PY_PIP="%ROOT_FOLDER%\python-envs\py37\interpreter\Scripts"
set PY_LIBS="%ROOT_FOLDER%\python-envs\py37\interpreter\Lib;%ROOT_FOLDER%\python-envs\py37\interpreter\Lib\site-packages"

%PYTHON_37_PYTHON_EXECUTABLE% -m pip install -r "%COMBINED_REQUIREMENTS%" --target "%ROOT_FOLDER%\python-envs\py37\deps"