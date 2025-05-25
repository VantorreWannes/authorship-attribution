from authorship_attribution._internal.features.average.words.lengths import AverageWordLengthFeature


from pytest import fixture, approx

from authorship_attribution._internal.features.extractors.average.words.lengths import (
    AverageWordLengthFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def sample_text() -> Text:
    return "This is a test text."


@fixture
def empty_text() -> Text:
    return ""


@fixture
def extractor(sample_text: Text) -> AverageWordLengthFeatureExtractor:
    return AverageWordLengthFeatureExtractor(sample_text)


@fixture
def empty_extractor(empty_text: Text) -> AverageWordLengthFeatureExtractor:
    return AverageWordLengthFeatureExtractor(empty_text)


def test_word_count(
    extractor: AverageWordLengthFeatureExtractor,
) -> None:
    assert extractor.word_count() == 6


def test_summed_word_lengths(
    extractor: AverageWordLengthFeatureExtractor,
) -> None:
    assert extractor.summed_word_lengths() == 16