from typing import Literal
from pytest import fixture, approx
from authorship_attribution._internal.features.average.sentences.words import (
    AverageSentenceLengthInWordsFeature,
)
from authorship_attribution._internal.types.aliases import Json


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
    return 10


@fixture
def json_data(word_count: int, sentence_count: int) -> Json:
    return {"word_count": word_count, "sentence_count": sentence_count}


@fixture
def average_word_length_feature(
    word_count: int, sentence_count: int
) -> AverageSentenceLengthInWordsFeature:
    return AverageSentenceLengthInWordsFeature(word_count, sentence_count)


def test_name(name: Literal["average_sentence_length_in_words_feature"]) -> None:
    assert AverageSentenceLengthInWordsFeature.name() == name


def test_file_name(
    file_name: Literal["average_sentence_length_in_words_feature.json"],
) -> None:
    assert AverageSentenceLengthInWordsFeature.file_name() == file_name


def test_to_json(
    average_word_length_feature: AverageSentenceLengthInWordsFeature, json_data: Json
) -> None:
    assert average_word_length_feature.to_json() == json_data


def test_from_json(json_data: Json, word_count: int, sentence_count: int) -> None:
    feature = AverageSentenceLengthInWordsFeature.from_json(json_data)
    assert isinstance(feature, AverageSentenceLengthInWordsFeature)
    assert feature.word_count == word_count
    assert feature.sentence_count == sentence_count


def test_average_calculation(
    average_word_length_feature: AverageSentenceLengthInWordsFeature,
) -> None:
    assert average_word_length_feature.average_sentence_length_in_words() == approx(
        10.0
    )


def test_average_calculation_zero_sentences() -> None:
    feature = AverageSentenceLengthInWordsFeature(word_count=0, sentence_count=0)
    assert feature.average_sentence_length_in_words() == approx(0.0)

    feature_with_words = AverageSentenceLengthInWordsFeature(
        word_count=50, sentence_count=0
    )
    assert feature_with_words.average_sentence_length_in_words() == approx(0.0)
