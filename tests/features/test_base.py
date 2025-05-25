from typing import Literal
from pytest import fixture
from authorship_attribution._internal.features.base.base import Feature
from authorship_attribution._internal.types.aliases import Json


@fixture
def feature_name_val() -> Literal["feature"]:
    return "feature"


@fixture
def feature_file_name_val() -> Literal["feature.json"]:
    return "feature.json"


@fixture
def empty_json_data() -> Json:
    return {}


@fixture
def base_feature_instance() -> Feature:
    return Feature()


def test_name(feature_name_val: Literal["feature"]) -> None:
    assert Feature.name() == feature_name_val


def test_file_name(feature_file_name_val: Literal["feature.json"]) -> None:
    assert Feature.file_name() == feature_file_name_val


def test_to_json(base_feature_instance: Feature, empty_json_data: Json) -> None:
    assert base_feature_instance.to_json() == empty_json_data


def test_from_json(empty_json_data: Json) -> None:
    feature_instance = Feature.from_json(empty_json_data)
    assert isinstance(feature_instance, Feature)
    assert feature_instance.to_json() == empty_json_data
