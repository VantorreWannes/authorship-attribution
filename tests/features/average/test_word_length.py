from typing import Any, Literal
from pytest import fixture
from authorship_attribution._internal.features.average.word_length import (
    AverageWordLengthFeature,
)
from authorship_attribution._internal.features.base.base import Feature


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
    return 1000


@fixture
def json(word_count: int, summed_word_lengths: int) -> dict[Any, Any]:
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


def test_to_json(average_word_length_feature: AverageWordLengthFeature, json) -> None:
    assert average_word_length_feature.to_json() == json


def test_from_json(json) -> None:
    assert AverageWordLengthFeature.from_json(json)
