# run in maya:
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

# run tests
```shell
run_all_tests.bat
```