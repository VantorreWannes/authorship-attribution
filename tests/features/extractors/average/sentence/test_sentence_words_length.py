from typing import Literal


from authorship_attribution._internal.features.extractors.average.sentence.words import (
    AverageSentenceLengthInWordsFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text
from pytest import fixture


@fixture
def text() -> Text:
    return "This is a test text. This is a test text."


@fixture
def word_count() -> Literal[12]:
    return 12


@fixture
def sentence_count() -> Literal[2]:
    return 2


@fixture
def average_sentence_length_in_words_feature_extractor(
    text: Text,
) -> AverageSentenceLengthInWordsFeatureExtractor:
    return AverageSentenceLengthInWordsFeatureExtractor(text)


def test_word_count(
    average_sentence_length_in_words_feature_extractor: AverageSentenceLengthInWordsFeatureExtractor,
    word_count: Literal[12],
) -> None:
    assert average_sentence_length_in_words_feature_extractor.word_count() == word_count


def test_sentence_count(
    average_sentence_length_in_words_feature_extractor: AverageSentenceLengthInWordsFeatureExtractor,
    sentence_count: Literal[2],
) -> None:
    assert (
        average_sentence_length_in_words_feature_extractor.sentence_count()
        == sentence_count
    )
