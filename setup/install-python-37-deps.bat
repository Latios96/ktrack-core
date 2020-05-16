setlocal
SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

SET PYTHON_37_PIP_EXECUTABLE="%ROOT_FOLDER%\python-envs\py37\interpreter\Scripts\pip.exe"

%PYTHON_37_PIP_EXECUTABLE% install -r "%ROOT_FOLDER%\requirements.txt" --target "%ROOT_FOLDER%\python-envs\py37\deps"
%PYTHON_37_PIP_EXECUTABLE% install -r "%ROOT_FOLDER%\requirements-dev.txt" --target "%ROOT_FOLDER%\python-envs\py37\deps"