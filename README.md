# Ktrack-core
My VFX Pipeline foundation. Contains:
- a Shotgun like Database
- folder creation tools
- path <-> context functionality (extract project, entity, task.. from file path)
- Shotgun Toolkit-like engine api

## Design decisions
- no per-project configuration: this can be done by batch files or package managers like rez
- no config file fiddling all the time
- no fancy package management like Shotgun Toolkit does, we rely on the standard python setup.py
- no db session / fancy ORM handling / running DB migrations, simple Shotgun like API
- unit tests coverage

## Install
```shell
python setup.py install
```

## Tests
run tests:
```shell
run_all_tests.bat
```
## run in maya:
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


