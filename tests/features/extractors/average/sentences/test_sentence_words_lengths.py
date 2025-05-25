from authorship_attribution._internal.features.average.sentences.words import AverageSentenceLengthInWordsFeature


from typing import Literal
from pytest import fixture, approx

from authorship_attribution._internal.features.extractors.average.sentences.words import (
    AverageSentenceLengthInWordsFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def sample_text() -> Text:
    return "This is a test text. This is another one."


@fixture
def empty_text() -> Text:
    return ""


@fixture
def expected_word_count() -> int:
    return 11


@fixture
def expected_sentence_count() -> Literal[2]:
    return 2


@fixture
def extractor(sample_text: Text) -> AverageSentenceLengthInWordsFeatureExtractor: # Renamed
    return AverageSentenceLengthInWordsFeatureExtractor(sample_text)


@fixture
def empty_extractor(empty_text: Text) -> AverageSentenceLengthInWordsFeatureExtractor:
    return AverageSentenceLengthInWordsFeatureExtractor(empty_text)


def test_word_count(
    extractor: AverageSentenceLengthInWordsFeatureExtractor,
    expected_word_count: int,
) -> None:
    assert extractor.word_count() == expected_word_count


def test_sentence_count(
    extractor: AverageSentenceLengthInWordsFeatureExtractor,
    expected_sentence_count: Literal[2],
) -> None:
    assert extractor.sentence_count() == expected_sentence_count


def test_feature_extraction(
    extractor: AverageSentenceLengthInWordsFeatureExtractor,
    expected_word_count: int,
    expected_sentence_count: Literal[2],
) -> None:
    feature: AverageSentenceLengthInWordsFeature = extractor.feature()
    assert feature.word_count == expected_word_count
    assert feature.sentence_count == expected_sentence_count
    assert feature.average_sentence_length_in_words() == approx(expected_word_count / expected_sentence_count)


def test_empty_text_extraction(empty_extractor: AverageSentenceLengthInWordsFeatureExtractor) -> None:
    assert empty_extractor.word_count() == 0
    assert empty_extractor.sentence_count() == 0
    feature: AverageSentenceLengthInWordsFeature = empty_extractor.feature()
    assert feature.word_count == 0
    assert feature.sentence_count == 0
    assert feature.average_sentence_length_in_words() == approx(0.0)