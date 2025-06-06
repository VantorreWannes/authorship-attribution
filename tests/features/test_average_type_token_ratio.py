from pytest import approx, fixture

from authorship_attribution._internals.features.average_type_token_ratio import (
    AverageTypeTokenRatioFeature,
    AverageTypeTokenRatioFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import Text


@fixture
def text() -> Text:
    return "hello my name is hello my name is"


@fixture
def unique_words_count() -> int:
    return 4


@fixture
def words_count() -> int:
    return 8


@fixture
def average_type_token_ratio() -> float:
    return 0.5


@fixture
def feature(unique_words_count: int, words_count: int) -> AverageTypeTokenRatioFeature:
    return AverageTypeTokenRatioFeature(unique_words_count, words_count)


@fixture
def feature_extractor(text: Text) -> AverageTypeTokenRatioFeatureExtractor:
    return AverageTypeTokenRatioFeatureExtractor(text)


def test_unique_words_count(
    feature_extractor: AverageTypeTokenRatioFeatureExtractor,
    unique_words_count: int,
) -> None:
    assert feature_extractor.unique_words_count() == unique_words_count


def test_words_count(
    feature_extractor: AverageTypeTokenRatioFeatureExtractor,
    words_count: int,
) -> None:
    assert feature_extractor.words_count() == words_count

def test_average_type_token_ratio(
    feature: AverageTypeTokenRatioFeature,
    average_type_token_ratio: float,
) -> None:
    assert feature.average_type_token_ratio() == approx(
        average_type_token_ratio, abs=0.01
    )