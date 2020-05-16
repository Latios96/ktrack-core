@echo off
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

%PYTHON_37_PYTHON_EXECUTABLE% -m pip install -r "%COMBINED_REQUIREMENTS%" --target "%ROOT_FOLDER%\python-envs\py37\deps"

echo python37.zip>> "%ROOT_FOLDER%\python-envs\py37\interpreter\python37._pth
echo .>> "%ROOT_FOLDER%\python-envs\py37\interpreter\python37._pth
echo %ROOT_FOLDER%\python-envs\py37\interpreter\Lib\site-packages>> "%ROOT_FOLDER%\python-envs\py37\interpreter\python37._pth
echo %ROOT_FOLDER%\python-envs\py37\deps>> "%ROOT_FOLDER%\python-envs\py37\interpreter\python37._pth
echo %ROOT_FOLDER%>> "%ROOT_FOLDER%\python-envs\py37\interpreter\python37._pth