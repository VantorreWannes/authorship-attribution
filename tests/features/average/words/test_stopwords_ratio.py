from typing import Literal
from pytest import fixture, approx

from authorship_attribution._internal.features.average.words.stopwords_ratio import (
    StopwordsRatioFeature,
)
from authorship_attribution._internal.types.aliases import Json


@fixture
def name() -> Literal["stopwords_ratio_feature"]:
    return "stopwords_ratio_feature"


@fixture
def file_name() -> Literal["stopwords_ratio_feature.json"]:
    return "stopwords_ratio_feature.json"


@fixture
def stopwords_count_val() -> int:
    return 25


@fixture
def total_word_count_val() -> int:
    return 100


@fixture
def json_data(stopwords_count_val: int, total_word_count_val: int) -> Json:
    return {
        "stopwords_count": stopwords_count_val,
        "total_word_count": total_word_count_val,
    }


@fixture
def stopwords_ratio_feature_instance(
    stopwords_count_val: int, total_word_count_val: int
) -> StopwordsRatioFeature:
    return StopwordsRatioFeature(stopwords_count_val, total_word_count_val)


def test_name(name: Literal["stopwords_ratio_feature"]) -> None:
    assert StopwordsRatioFeature.name() == name


def test_file_name(file_name: Literal["stopwords_ratio_feature.json"]) -> None:
    assert StopwordsRatioFeature.file_name() == file_name


def test_to_json(
    stopwords_ratio_feature_instance: StopwordsRatioFeature, json_data: Json
) -> None:
    assert stopwords_ratio_feature_instance.to_json() == json_data


def test_from_json(
    json_data: Json, stopwords_count_val: int, total_word_count_val: int
) -> None:
    feature = StopwordsRatioFeature.from_json(json_data)
    assert isinstance(feature, StopwordsRatioFeature)
    assert feature.stopwords_count == stopwords_count_val
    assert feature.total_word_count == total_word_count_val


def test_ratio_calculation(
    stopwords_ratio_feature_instance: StopwordsRatioFeature,
) -> None:
    assert stopwords_ratio_feature_instance.stopwords_ratio() == approx(0.25)


def test_ratio_calculation_zero_total_words() -> None:
    feature_zero_all = StopwordsRatioFeature(stopwords_count=0, total_word_count=0)
    assert feature_zero_all.stopwords_ratio() == approx(0.0)

    feature_stopwords_no_total = StopwordsRatioFeature(
        stopwords_count=5, total_word_count=0
    )
    assert feature_stopwords_no_total.stopwords_ratio() == approx(0.0)
