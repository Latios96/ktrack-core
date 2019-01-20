# ktrack-core
Tool to track assets, shots, tasks and workfiles for a CGI movie production.
Offers automatic folder and file creation and an API to query the database.

For usage see https://github.com/Latios96/ktrack-core/wiki/Ktrack-Command

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

## run ktrack in maya:
start engine
```python
import kttk
from kttk.engines import maya_engine
kttk.engines.start_engine(maya_engine.MayaEngine)
```
run file manager
```python
from kttk_widgets import file_manager_view
w = file_manager_view.FileManagerWidget()
w.show()
```
