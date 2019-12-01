# coding=utf-8
from kttk import name_sanitizer


def test_sanitize_name():
    # test spaces

    name = name_sanitizer.sanitize_name("name with spaces")

    assert " " not in name

    # test invalid characters
    test_str = "<>:.?/\\|* \"'"
    name = name_sanitizer.sanitize_name(test_str)

    for char in test_str:
        assert char not in name

    # test german umlaute
    name = name_sanitizer.sanitize_name("täÄstPröÖjüÜkßts")

    umlaute_mapping = {
        'ä': 'ae',
        'A': 'AE',
        'ö': 'oe',
        'Ö': 'OE',
        'ü': 'ue',
        'Ü': 'UE',
        'ß': 'ss'
    }

    for key, value in umlaute_mapping.items():
        assert key not in name

    # test no multiple underscores
    name = name_sanitizer.sanitize_name("test__pr<oje|ct____is_aw_?esome")

    assert name == "test_pr_oje_ct_is_aw_esome"
