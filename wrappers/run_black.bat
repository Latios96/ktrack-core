@echo off
setlocal

SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

"%ROOT_FOLDER%\python-envs\py37\interpreter\python.exe" -m black "%ROOT_FOLDER%\kttk" "%ROOT_FOLDER%\ktrack_api" "%ROOT_FOLDER%\kttk_widgets"