import pytest

from kttk.references.entity_types import ReferenceEntityType
from kttk.references.workfile_reference import SerializedWorkfileReference
from kttk.references.workfile_reference_parser import SerializedWorkfileReferenceParser


def test_should_parse_asset_with_latest():
    parser = SerializedWorkfileReferenceParser()

    serialized_reference = parser.parse("snow_globe:a:rheinturm:modelling:latest")

    assert serialized_reference == SerializedWorkfileReference(
        project_name="snow_globe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="rheinturm",
        task_name="modelling",
        version_identifier="latest",
    )


def test_should_parse_shot_with_latest():
    parser = SerializedWorkfileReferenceParser()

    serialized_reference = parser.parse("snow_globe:sh:rheinturm:modelling:latest")

    assert serialized_reference == SerializedWorkfileReference(
        project_name="snow_globe",
        entity_type=ReferenceEntityType.SHOT,
        entity_name="rheinturm",
        task_name="modelling",
        version_identifier="latest",
    )


def test_should_parse_asset_with_version():
    parser = SerializedWorkfileReferenceParser()

    serialized_reference = parser.parse("snow_globe:a:rheinturm:modelling:v009")

    assert serialized_reference == SerializedWorkfileReference(
        project_name="snow_globe",
        entity_type=ReferenceEntityType.ASSET,
        entity_name="rheinturm",
        task_name="modelling",
        version_identifier="v009",
    )


def test_should_not_parse_invalid_entity_type():
    parser = SerializedWorkfileReferenceParser()

    with pytest.raises(ValueError):
        parser.parse("snow_globe:sdaert:rheinturm:modelling:v009")


def test_should_not_parse_invalid_version_identifier():
    parser = SerializedWorkfileReferenceParser()

    with pytest.raises(ValueError):
        parser.parse("snow_globe:sh:rheinturm:modelling:ysgfd")
