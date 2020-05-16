setlocal
SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

set PYTHON_37_ZIP="%~dp0temp\python-3.7.7-embed-win32.zip"

if exist %PYTHON_37_ZIP% (
    echo Skipping Python 37 Download
) else (
    echo Downloading Python 37
    mkdir "%~dp0temp"
    bitsadmin /transfer downloadpython /download /priority high "https://www.python.org/ftp/python/3.7.7/python-3.7.7-embed-win32.zip" %PYTHON_37_ZIP%
)

SET PYTHON_37_INTERPRETER_EXECUTABLE="%ROOT_FOLDER%\python-envs\py37\interpreter\python.exe"

if exist %PYTHON_37_INTERPRETER_EXECUTABLE% (
    echo Skipping Python 37 Install
) else (
    echo Unzip Python 37..
    tar -C "%ROOT_FOLDER%\python-envs\py37\interpreter" -xf %PYTHON_37_ZIP%
    echo Unzipped Python 37
)

set GET_PIP_PATH="%~dp0temp\get-pip.py"

if exist %GET_PIP_PATH% (
    echo Skipping pip Download
) else (
    echo Downloading pip
    bitsadmin /transfer downloadpython /download /priority high "https://bootstrap.pypa.io/get-pip.py" %GET_PIP_PATH%
)

if exist "%ROOT_FOLDER%\python-envs\py37\interpreter\Scripts\pip.exe" (
    echo Skipping pip Install
) else (
    echo Install pip
    %PYTHON_37_INTERPRETER_EXECUTABLE% %GET_PIP_PATH%
    echo %ROOT_FOLDER%\python-envs\py37\interpreter\Lib\site-packages>> "%ROOT_FOLDER%\python-envs\py37\interpreter\python37._pth
    echo %ROOT_FOLDER%\python-envs\py37\deps>> "%ROOT_FOLDER%\python-envs\py37\interpreter\python37._pth
)



