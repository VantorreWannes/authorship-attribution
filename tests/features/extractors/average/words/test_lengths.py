from pytest import fixture

from authorship_attribution._internal.features.extractors.average.words.lengths import (
    AverageWordLengthFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def sample_text() -> Text:
    return "This is a test text."


@fixture
def extractor(sample_text: Text) -> AverageWordLengthFeatureExtractor:
    return AverageWordLengthFeatureExtractor(sample_text)


def test_word_count(
    extractor: AverageWordLengthFeatureExtractor,
) -> None:
    assert extractor.word_count() == 5


def test_summed_word_lengths(
    extractor: AverageWordLengthFeatureExtractor,
) -> None:
    assert extractor.summed_word_lengths() == 15
