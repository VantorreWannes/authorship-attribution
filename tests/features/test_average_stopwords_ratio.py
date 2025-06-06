from pytest import approx, fixture
from authorship_attribution._internals.features.average_stopwords_ratio import (
    AverageStopwordsRatioFeature,
    AverageStopwordsRatioFeatureExtractor,
)


@fixture
def text() -> str:
    return "This is a test sentence with some stopwords"


@fixture
def stopwords_count() -> int:
    return 4


@fixture
def words_count() -> int:
    return 8


@fixture
def average_stopwords_ratio() -> float:
    return 0.5


@fixture
def feature(stopwords_count: int, words_count: int) -> AverageStopwordsRatioFeature:
    return AverageStopwordsRatioFeature(stopwords_count, words_count)


@fixture
def feature_extractor(text: str) -> AverageStopwordsRatioFeatureExtractor:
    return AverageStopwordsRatioFeatureExtractor(text)


def test_stopwords_count(
    feature_extractor: AverageStopwordsRatioFeatureExtractor,
    stopwords_count: int,
) -> None:
    assert feature_extractor.stopwords_count() == stopwords_count


def test_words_count(
    feature_extractor: AverageStopwordsRatioFeatureExtractor,
    words_count: int,
) -> None:
    assert feature_extractor.words_count() == words_count


def test_average_stopwords_ratio(
    feature: AverageStopwordsRatioFeature,
    average_stopwords_ratio: float,
) -> None:
    assert feature.average_stopwords_ratio() == approx(
        average_stopwords_ratio, abs=0.01
    )
