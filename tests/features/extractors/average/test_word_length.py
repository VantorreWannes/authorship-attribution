from authorship_attribution._internal.features.extractors.average.word_length import (
    AverageWordLengthFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text
from pytest import fixture


@fixture
def text() -> Text:
    return "This is a test text."


@fixture
def average_word_length_feature_extractor(
    text: Text,
) -> AverageWordLengthFeatureExtractor:
    return AverageWordLengthFeatureExtractor(text)


def test_word_count(
    average_word_length_feature_extractor: AverageWordLengthFeatureExtractor,
) -> None:
    assert average_word_length_feature_extractor.word_count() == 6


def test_summed_word_lengths(
    average_word_length_feature_extractor: AverageWordLengthFeatureExtractor,
) -> None:
    assert average_word_length_feature_extractor.summed_word_lengths() == 16
