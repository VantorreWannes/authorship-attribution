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


def test_feature_extraction(extractor: AverageWordLengthFeatureExtractor) -> None:
    feature: AverageWordLengthFeature = extractor.feature()
    assert feature.word_count == 6
    assert feature.summed_word_lengths == 16
    assert feature.average_word_length() == approx(16 / 6)


def test_empty_text_extraction(
    empty_extractor: AverageWordLengthFeatureExtractor,
) -> None:
    assert empty_extractor.word_count() == 0
    assert empty_extractor.summed_word_lengths() == 0
    feature: AverageWordLengthFeature = empty_extractor.feature()
    assert feature.word_count == 0
    assert feature.summed_word_lengths == 0
    assert feature.average_word_length() == approx(0.0)
