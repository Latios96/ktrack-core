import pytest

from kttk.references.entity_types import ReferenceEntityType
from kttk.references.serialized_task_reference_parser import (
    SerializedTaskReferenceParser,
)
from kttk.references.task_reference import SerializedTaskReference


def test_should_parse_asset_with_latest():
    parser = SerializedTaskReferenceParser()

    serialized_reference = parser.parse("snow_globe:a:rheinturm:modelling")

    assert serialized_reference == SerializedTaskReference(
        project_name="snow_globe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="rheinturm",
        task_name="modelling",
    )


def test_should_parse_shot():
    parser = SerializedTaskReferenceParser()

    serialized_reference = parser.parse("snow_globe:sh:rheinturm:modelling")

    assert serialized_reference == SerializedTaskReference(
        project_name="snow_globe",
        entity_type=ReferenceEntityType.SHOT,
        entity_name="rheinturm",
        task_name="modelling",
    )


def test_should_parse_asset_with_version():
    parser = SerializedTaskReferenceParser()

    serialized_reference = parser.parse("snow_globe:a:rheinturm:modelling")

    assert serialized_reference == SerializedTaskReference(
        project_name="snow_globe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="rheinturm",
        task_name="modelling",
    )


def test_should_not_parse_invalid_entity_type():
    parser = SerializedTaskReferenceParser()

    with pytest.raises(ValueError):
        parser.parse("snow_globe:sdaert:rheinturm:modelling")
