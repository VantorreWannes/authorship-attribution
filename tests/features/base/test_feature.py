from pytest_mock import MockFixture

from authorship_attribution._internal.features.base.base import Feature


def test_name() -> None:
    assert Feature.name() == "feature"


def test_file_name() -> None:
    assert Feature.file_name() == "feature.json"


def test_from_file(
    mocker: MockFixture,
) -> None:
    mock_from_json = mocker.patch(
        "authorship_attribution._internal.features.base.base.Feature.from_json"
    )
    mocker.patch("builtins.open", mocker.mock_open(read_data="{}"))
    Feature.from_file("")
    mock_from_json.assert_called_once_with({})
