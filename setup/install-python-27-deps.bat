@echo off
setlocal
SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

SET PYTHON_27_PIP_EXECUTABLE="%ROOT_FOLDER%\python-envs\py27\interpreter\Scripts\pip.exe"

SET COMBINED_REQUIREMENTS="%~dp0temp\requirements-combined.txt"
type "%ROOT_FOLDER%\requirements.txt" > "%COMBINED_REQUIREMENTS%"
echo. >> "%COMBINED_REQUIREMENTS%"
type "%ROOT_FOLDER%\requirements-dev.txt" >> "%COMBINED_REQUIREMENTS%"

%PYTHON_27_PIP_EXECUTABLE% install -r "%COMBINED_REQUIREMENTS%" --target "%ROOT_FOLDER%\python-envs\py27\deps"