setlocal

SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

set PY_PIP="%ROOT_FOLDER%\python-envs\py37\interpreter\Scripts"
set PY_LIBS="%ROOT_FOLDER%\python-envs\py37\interpreter\Lib;%ROOT_FOLDER%\python-envs\py37\interpreter\Lib\site-packages;%ROOT_FOLDER%\python-envs\py37\deps"

"%ROOT_FOLDER%\python-envs\py37\interpreter\python.exe" %*