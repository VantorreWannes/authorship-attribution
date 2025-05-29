from pytest import fixture

from authorship_attribution._internal.features.extractors.average.punctuation_frequencies import (
    PunctuationFrequenciesFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def sample_text() -> Text:
    return ".,,;;;"


@fixture
def extractor(sample_text: Text) -> PunctuationFrequenciesFeatureExtractor:
    return PunctuationFrequenciesFeatureExtractor(sample_text)


def test_punctuation_counts(extractor: PunctuationFrequenciesFeatureExtractor) -> None:
    assert extractor.punctuation_counts() == {".": 1, ",": 2, ";": 3}


def test_total_punctuation_count(
    extractor: PunctuationFrequenciesFeatureExtractor,
) -> None:
    assert extractor.total_punctuation_count() == 6
