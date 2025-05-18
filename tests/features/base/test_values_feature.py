from typing import Literal
from _pytest.fixtures import fixture
from authorship_attribution._internal.features.base.values import ValuesFeature


@fixture
def data() -> Literal["hello"]:
    return "hello"

@fixture
def json(data: str) -> dict[str, str]:
    return {"value": data}

@fixture
def values_feature(data) -> ValuesFeature:
    return ValuesFeature(value=data)


def test_name() -> None:
    assert ValuesFeature.name() == "values_feature"


def test_file_name() -> None:
    assert ValuesFeature.file_name() == "values_feature.json"


def test_to_json(values_feature: ValuesFeature, json: dict[str, str]) -> None:
    assert values_feature.to_json() == json


def test_from_json(json: dict[str, str]) -> None:
    assert ValuesFeature.from_json(json).to_json() == json