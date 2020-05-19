# ktrack-core
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
![Python CI](https://github.com/Latios96/ktrack-core/workflows/Python%20CI/badge.svg)

Tool to track assets, shots, tasks and workfiles for a CGI movie production.
Offers automatic folder and file creation and an API to query the database.

## Getting started
```shell
virtualenv venv
./venv/bin/activate
python setup.py install
```

## Run the tests
### Standart python tests
```shell
python run_tests.py
```
### Run the test inside of the DCCs
```shell
run_tests_maya.bat
run_tests_nuke.bat
run_tests_houdini.bat
```
or everything:
```shell
run_all_tests.bat
```

