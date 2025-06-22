from collections import Counter
from pytest import approx, fixture

from authorship_attribution._internals.features.average_character_ngram_frequencies import (
    AverageCharacterNgramFrequenciesFeature,
    AverageCharacterNgramFrequenciesFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import NGram, Text


@fixture
def text() -> Text:
    return "abcabcabc"


@fixture
def ngram_size() -> int:
    return 3


@fixture
def character_ngram_counts() -> Counter[NGram]:
    return Counter({"abc": 3, "bca": 2, "cab": 2})


@fixture
def all_character_ngrams_count() -> int:
    return 7


@fixture
def average_character_ngram_frequencies() -> dict[NGram, float]:
    return {"abc": 3 / 7, "bca": 2 / 7, "cab": 2 / 7}


@fixture
def feature(
    character_ngram_counts: Counter[NGram], all_character_ngrams_count: int
) -> AverageCharacterNgramFrequenciesFeature:
    return AverageCharacterNgramFrequenciesFeature(
        character_ngram_counts, all_character_ngrams_count
    )


@fixture
def feature_extractor(
    text: Text, ngram_size: int
) -> AverageCharacterNgramFrequenciesFeatureExtractor:
    return AverageCharacterNgramFrequenciesFeatureExtractor(text, ngram_size)


def test_character_ngram_counts(
    feature_extractor: AverageCharacterNgramFrequenciesFeatureExtractor,
    character_ngram_counts: Counter[NGram],
) -> None:
    assert feature_extractor.character_ngram_counts() == character_ngram_counts


def test_all_character_ngrams_count(
    feature_extractor: AverageCharacterNgramFrequenciesFeatureExtractor,
    all_character_ngrams_count: int,
) -> None:
    assert feature_extractor.all_character_ngrams_count() == all_character_ngrams_count


def test_average_character_ngram_frequencies(
    feature: AverageCharacterNgramFrequenciesFeature,
    average_character_ngram_frequencies: dict[NGram, float],
) -> None:
    assert feature.character_ngram_frequencies() == approx(
        expected=average_character_ngram_frequencies
    )
