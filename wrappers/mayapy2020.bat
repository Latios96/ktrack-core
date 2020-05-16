@echo off
setlocal

SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

set PYTHONPATH=%ROOT_FOLDER%\python-envs\py27\deps;%ROOT_FOLDER%

"C:\Program Files\Autodesk\Maya2020\bin\mayapy.exe"