from typing import Any, Literal
from pytest import fixture
from authorship_attribution._internal.features.average.words.type_token_ratio import (
    TypeTokenRatioFeature,
)


@fixture
def name() -> Literal["type_token_ratio_feature"]:
    return "type_token_ratio_feature"


@fixture
def file_name() -> Literal["type_token_ratio_feature.json"]:
    return "type_token_ratio_feature.json"


@fixture
def unique_words_count() -> int:
    return 100


@fixture
def all_words_count() -> int:
    return 1000


@fixture
def json(unique_words_count: int, all_words_count: int) -> dict[Any, Any]:
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


def test_to_json(type_token_ratio_feature: TypeTokenRatioFeature, json) -> None:
    assert type_token_ratio_feature.to_json() == json


def test_from_json(json) -> None:
    assert TypeTokenRatioFeature.from_json(json)
