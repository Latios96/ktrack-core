setlocal
SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

SET PYTHON_27_PIP_EXECUTABLE="%ROOT_FOLDER%\python-envs\py27\interpreter\Scripts\pip.exe"

%PYTHON_27_PIP_EXECUTABLE% install -r "%ROOT_FOLDER%\requirements.txt" --target "%ROOT_FOLDER%\python-envs\py27\deps"
%PYTHON_27_PIP_EXECUTABLE% install -r "%ROOT_FOLDER%\requirements-dev.txt" --target "%ROOT_FexitrOLDER%\python-envs\py27\deps"