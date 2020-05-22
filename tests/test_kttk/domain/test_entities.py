import pytest

from kttk.domain.entities import CutInformation, VersionNumber


class TestCutInformation(object):
    def test_correct_cut_duration(self):
        cut_information = CutInformation(cut_in=1000, cut_out=1050)
        assert cut_information.cut_duration == 50

    def test_correct_frame_count(self):
        cut_information = CutInformation(cut_in=1000, cut_out=1050)
        assert cut_information.frame_count == 51


class TestVersionNumber(object):
    @pytest.mark.parametrize(
        "version_identifier,version_number", [("v001", 1), ("001", 1), ("1", 1), (1, 1)]
    )
    def test_parse_correct(self, version_identifier, version_number):
        version = VersionNumber(version_identifier)
        assert version.number == version_number

    @pytest.mark.parametrize(
        "version_identifier", ["v000", "v1000", "abc", "wurst", None]
    )
    def test_parse_incorrect(self, version_identifier):
        with pytest.raises(ValueError):
            assert VersionNumber(version_identifier)

    def test_correct_version_string(self):
        version = VersionNumber(1)
        assert version.version_str == "v001"

    def test_correct_range(self):
        assert VersionNumber(1)
        assert VersionNumber(999)

        with pytest.raises(ValueError):
            assert VersionNumber(0)
        with pytest.raises(ValueError):
            assert VersionNumber(-1)
        with pytest.raises(ValueError):
            assert VersionNumber(1000)

    def test_increase_success(self):
        version = VersionNumber()
        assert version.increase().number == version.number + 1

        version = VersionNumber(100)
        increased_version = version.increase()
        assert increased_version.number == 101

    def test_increase_reach_limit(self):
        with pytest.raises(ValueError):
            VersionNumber(999).increase()

    def test_str(self):
        version = VersionNumber(12)
        assert str(version) == "v012"
