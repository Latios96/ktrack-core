import pytest

from kttk import utils


def test_entity_id_dict():
    # test valid entity

    d = utils.entity_id_dict({'type': 'shot', 'id': 123, 'code': 'awesome'})
    assert len(d.keys()) == 2
    assert d['type'] == 'shot'
    assert d['id'] == 123

    # test None
    assert utils.entity_id_dict(None) == None

    # test invalid entity
    # missing id
    with pytest.raises(KeyError):
        utils.entity_id_dict({'type': 'shot', 'ied': 123, 'code': 'awesome'})

    # missing type
    with pytest.raises(KeyError):
        utils.entity_id_dict({'typ': 'shot', 'id': 123, 'code': 'awesome'})

    # missing type and id
    with pytest.raises(KeyError):
        utils.entity_id_dict({'tyepe': 'shot', 'ied': 123, 'code': 'awesome'})
