setlocal
SET OLD_DIRECTORY=%CD%
cd %~dp0
cd ..
SET ROOT_FOLDER=%CD%
cd %OLD_DIRECTORY%

set PYTHON_27_INSTALLER="%~dp0temp\python-2.7.16.amd64.msi"

if exist %PYTHON_27_INSTALLER% (
    echo Skipping Python 27 Download
) else (
    echo Downloading Python 27
    mkdir "%~dp0temp"
    bitsadmin /transfer downloadpython /download /priority normal "https://www.python.org/ftp/python/2.7.16/python-2.7.16.amd64.msi" %PYTHON_27_INSTALLER%
)

SET PYTHON_27_INTERPRETER_EXECUTABLE="%ROOT_FOLDER%\python-envs\py27\interpreter\python.exe"

if exist %PYTHON_27_INTERPRETER_EXECUTABLE% (
    echo Skipping Python 27 Install
) else (
    echo Install Python 27
    msiexec /a %PYTHON_27_INSTALLER% /quiet TARGETDIR="%ROOT_FOLDER%\python-envs\py27\interpreter"
)

set GET_PIP_PATH="%~dp0temp\get-pip.py"

if exist %GET_PIP_PATH% (
    echo Skipping pip Download
) else (
    echo Downloading pip
    bitsadmin /transfer downloadpython /download /priority high "https://bootstrap.pypa.io/get-pip.py" %GET_PIP_PATH%
)

if exist "%ROOT_FOLDER%\python-envs\py27\interpreter\Scripts\pip.exe" (
    echo Skipping pip Install
) else (
    echo Install pip
    %PYTHON_27_INTERPRETER_EXECUTABLE% %GET_PIP_PATH%
)





