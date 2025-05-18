from typing import Any, Literal
from pytest import fixture
from authorship_attribution._internal.features.base.base import Feature


@fixture
def name() -> Literal["feature"]:
    return "feature"


@fixture
def file_name() -> Literal["feature.json"]:
    return "feature.json"


@fixture
def json() -> dict[Any, Any]:
    return {}


@fixture
def feature() -> Feature:
    return Feature()


def test_name(name: Literal["feature"]) -> None:
    assert Feature.name() == name


def test_file_name(file_name: Literal["feature.json"]) -> None:
    assert Feature.file_name() == file_name


def test_to_json(json) -> None:
    assert Feature().to_json() == json


def test_from_json(json) -> None:
    assert Feature.from_json(json)
