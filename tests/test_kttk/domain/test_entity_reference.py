import pytest

from kttk.domain.entity_reference import EntityReference


def test_should_parse_entity_reference():
    entity_reference = EntityReference.parse("test_project:test_asset")

    assert entity_reference == EntityReference("test_project", "test_asset")


@pytest.mark.parametrize(
    "invalid_reference", ["test_project:test_asset:wr", "", None, "test"]
)
def test_should_not_parse_entity_reference(invalid_reference):
    with pytest.raises(ValueError):
        entity_reference = EntityReference.parse(invalid_reference)
