import pymel.core as pm
import pytest
import os

pytest.main(['-x', os.path.join(os.getcwd(), 'tests')])
pytest.main(['-x', os.path.join(os.getcwd(), 'tests_maya')])
pytest.main(['-x', os.path.join(os.getcwd(), 'test_kttk_widgets')])