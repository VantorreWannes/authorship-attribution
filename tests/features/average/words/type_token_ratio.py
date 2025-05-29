from typing import Literal
from pytest import fixture, approx
from authorship_attribution._internal.features.average.words.type_token_ratio import (
    TypeTokenRatioFeature,
)
from authorship_attribution._internal.types.aliases import Json


@fixture
def name() -> Literal["type_token_ratio_feature"]:
    return "type_token_ratio_feature"


@fixture
def file_name() -> Literal["type_token_ratio_feature.json"]:
    return "type_token_ratio_feature.json"


@fixture
def unique_words_count() -> int:
    return 50


@fixture
def all_words_count() -> int:
    return 100


@fixture
def json_data(unique_words_count: int, all_words_count: int) -> Json:
    return {
        "unique_words_count": unique_words_count,
        "all_words_count": all_words_count,
    }


@fixture
def type_token_ratio_feature(
    unique_words_count: int, all_words_count: int
) -> TypeTokenRatioFeature:
    return TypeTokenRatioFeature(unique_words_count, all_words_count)


def test_name(name: Literal["type_token_ratio_feature"]) -> None:
    assert TypeTokenRatioFeature.name() == name


def test_file_name(file_name: Literal["type_token_ratio_feature.json"]) -> None:
    assert TypeTokenRatioFeature.file_name() == file_name


def test_to_json(
    type_token_ratio_feature: TypeTokenRatioFeature, json_data: Json
) -> None:
    assert type_token_ratio_feature.to_json() == json_data


def test_from_json(
    json_data: Json, unique_words_count: int, all_words_count: int
) -> None:
    feature = TypeTokenRatioFeature.from_json(json_data)
    assert isinstance(feature, TypeTokenRatioFeature)
    assert feature.unique_words_count == unique_words_count
    assert feature.all_words_count == all_words_count


def test_ratio_calculation(type_token_ratio_feature: TypeTokenRatioFeature) -> None:
    assert type_token_ratio_feature.type_token_ratio() == approx(0.5)


def test_ratio_calculation_zero_words() -> None:
    feature = TypeTokenRatioFeature(unique_words_count=0, all_words_count=0)
    assert feature.type_token_ratio() == approx(0.0)

    feature_with_unique = TypeTokenRatioFeature(
        unique_words_count=10, all_words_count=0
    )
    assert feature_with_unique.type_token_ratio() == approx(0.0)
