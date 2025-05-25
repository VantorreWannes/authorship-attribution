from typing import Literal
from pytest import fixture, approx
from authorship_attribution._internal.features.average.words.lengths import (
    AverageWordLengthFeature,
)
from authorship_attribution._internal.types.aliases import Json


@fixture
def name() -> Literal["average_word_length_feature"]:
    return "average_word_length_feature"


@fixture
def file_name() -> Literal["average_word_length_feature.json"]:
    return "average_word_length_feature.json"


@fixture
def word_count() -> int:
    return 100


@fixture
def summed_word_lengths() -> int:
    return 500


@fixture
def json_data(word_count: int, summed_word_lengths: int) -> Json:
    return {"word_count": word_count, "summed_word_lengths": summed_word_lengths}


@fixture
def average_word_length_feature(
    word_count: int, summed_word_lengths: int
) -> AverageWordLengthFeature:
    return AverageWordLengthFeature(word_count, summed_word_lengths)


def test_name(name: Literal["average_word_length_feature"]) -> None:
    assert AverageWordLengthFeature.name() == name


def test_file_name(file_name: Literal["average_word_length_feature.json"]) -> None:
    assert AverageWordLengthFeature.file_name() == file_name


def test_to_json(
    average_word_length_feature: AverageWordLengthFeature, json_data: Json
) -> None:
    assert average_word_length_feature.to_json() == json_data


def test_from_json(json_data: Json, word_count: int, summed_word_lengths: int) -> None:
    feature = AverageWordLengthFeature.from_json(json_data)
    assert isinstance(feature, AverageWordLengthFeature)
    assert feature.word_count == word_count
    assert feature.summed_word_lengths == summed_word_lengths


def test_average_calculation(
    average_word_length_feature: AverageWordLengthFeature,
) -> None:
    assert average_word_length_feature.average_word_length() == approx(5.0)


def test_average_calculation_zero_words() -> None:
    feature = AverageWordLengthFeature(word_count=0, summed_word_lengths=0)
    assert feature.average_word_length() == approx(0.0)

    feature_with_lengths = AverageWordLengthFeature(
        word_count=0, summed_word_lengths=50
    )
    assert feature_with_lengths.average_word_length() == approx(0.0)
