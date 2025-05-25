from typing import Any, Literal
from pytest import fixture
from authorship_attribution._internal.features.average.sentences.words import (
    AverageSentenceLengthInWordsFeature,
)


@fixture
def name() -> Literal["average_sentence_length_in_words_feature"]:
    return "average_sentence_length_in_words_feature"


@fixture
def file_name() -> Literal["average_sentence_length_in_words_feature.json"]:
    return "average_sentence_length_in_words_feature.json"


@fixture
def word_count() -> int:
    return 100


@fixture
def sentence_count() -> int:
    return 1000


@fixture
def json(word_count: int, sentence_count: int) -> dict[Any, Any]:
    return {"word_count": word_count, "sentence_count": sentence_count}


@fixture
def average_word_length_feature(
    word_count: int, sentence_count: int
) -> AverageSentenceLengthInWordsFeature:
    return AverageSentenceLengthInWordsFeature(word_count, sentence_count)


def test_name(name: Literal["average_sentence_length_in_words_feature"]) -> None:
    assert AverageSentenceLengthInWordsFeature.name() == name


def test_file_name(file_name: Literal["average_sentence_length_in_words_feature.json"]) -> None:
    assert AverageSentenceLengthInWordsFeature.file_name() == file_name


def test_to_json(
    average_word_length_feature: AverageSentenceLengthInWordsFeature, json
) -> None:
    assert average_word_length_feature.to_json() == json


def test_from_json(json) -> None:
    assert AverageSentenceLengthInWordsFeature.from_json(json)
