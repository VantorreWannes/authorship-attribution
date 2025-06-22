from collections import Counter
from pytest import approx, fixture
from authorship_attribution._internals.types.aliases import Punctuation

from authorship_attribution._internals.features.average_punctuation_frequencies import (
    AveragePunctuationFrequenciesFeature,
    AveragePunctuationFrequenciesFeatureExtractor,
)


@fixture
def text() -> str:
    return "Hello! World, how are you?"


@fixture
def punctuation_counts() -> Counter[Punctuation]:
    return Counter[Punctuation]({"!": 1, ",": 1, "?": 1})


@fixture
def all_punctuations_count() -> int:
    return 3


@fixture
def average_punctuation_frequencies() -> dict[Punctuation, float]:
    return {"!": 0.33, ",": 0.33, "?": 0.33}


@fixture
def feature(
    punctuation_counts: Counter[Punctuation], all_punctuations_count: int
) -> AveragePunctuationFrequenciesFeature:
    return AveragePunctuationFrequenciesFeature(
        punctuation_counts, all_punctuations_count
    )


@fixture
def feature_extractor(text: str) -> AveragePunctuationFrequenciesFeatureExtractor:
    return AveragePunctuationFrequenciesFeatureExtractor(text)


def test_punctuation_counts(
    feature_extractor: AveragePunctuationFrequenciesFeatureExtractor,
    punctuation_counts: Counter[Punctuation],
) -> None:
    assert feature_extractor.punctuation_counts() == punctuation_counts


def test_all_punctuations_count(
    feature_extractor: AveragePunctuationFrequenciesFeatureExtractor,
    all_punctuations_count: int,
) -> None:
    assert feature_extractor.all_punctuations_count() == all_punctuations_count


def test_average_punctuation_frequencies(
    feature: AveragePunctuationFrequenciesFeature,
    average_punctuation_frequencies: dict[Punctuation, float],
) -> None:
    assert feature.average_pos_tag_frequencies() == approx(
        average_punctuation_frequencies, abs=0.01
    )
