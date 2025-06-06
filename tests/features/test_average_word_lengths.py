from pytest import approx, fixture

from authorship_attribution._internals.features.average_word_lengths import (
    AverageWordLengthFeature,
    AverageWordLengthFeatureExtractor,
)


@fixture
def text() -> str:
    return "hello i am wannes"


@fixture
def summed_word_lengths() -> int:
    return 14


@fixture
def words_count() -> int:
    return 4


@fixture
def average_word_length() -> float:
    return 3.5


@fixture
def feature(summed_word_lengths: int, words_count: int) -> AverageWordLengthFeature:
    return AverageWordLengthFeature(summed_word_lengths, words_count)


@fixture
def feature_extractor(text: str) -> AverageWordLengthFeatureExtractor:
    return AverageWordLengthFeatureExtractor(text)


def test_summed_word_lengths(
    feature_extractor: AverageWordLengthFeatureExtractor,
    summed_word_lengths: int,
) -> None:
    assert feature_extractor.summed_word_lengths() == summed_word_lengths


def test_words_count(
    feature_extractor: AverageWordLengthFeatureExtractor,
    words_count: int,
) -> None:
    assert feature_extractor.words_count() == words_count


def test_average_word_length(
    feature: AverageWordLengthFeature,
    average_word_length: float,
) -> None:
    assert feature.average_word_length() == approx(average_word_length, abs=0.01)
