call venv/scripts/activate
echo running regular tests...
pytest --junitxml=junit_xml_test_core.xml -o junit_suite_name=test_core
echo running widgets tests...
pytest -x test_kttk_widgets --junitxml=junit_xml_test_kttk_widgets.xml -o junit_suite_name=test_kttk_widgets