from collections import Counter
from pytest import approx, fixture

from authorship_attribution._internals.features.average_word_ngram_frequencies import (
    AverageWordNgramFrequenciesFeature,
    AverageWordNgramFrequenciesFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import NGram, Text


@fixture
def text() -> Text:
    return "one two one two three"


@fixture
def ngram_size() -> int:
    return 2


@fixture
def word_ngram_counts() -> Counter[NGram]:
    return Counter[NGram]({"onetwo": 2, "twoone": 1, "twothree": 1})


@fixture
def all_word_ngrams_count() -> int:
    return 4


@fixture
def average_word_ngram_frequencies() -> dict[NGram, float]:
    return {"onetwo": 0.5, "twoone": 0.25, "twothree": 0.25}


@fixture
def feature(
    word_ngram_counts: Counter[NGram], all_word_ngrams_count: int
) -> AverageWordNgramFrequenciesFeature:
    return AverageWordNgramFrequenciesFeature(word_ngram_counts, all_word_ngrams_count)


@fixture
def feature_extractor(
    text: Text, ngram_size: int
) -> AverageWordNgramFrequenciesFeatureExtractor:
    return AverageWordNgramFrequenciesFeatureExtractor(text, ngram_size)


def test_word_ngram_counts(
    feature_extractor: AverageWordNgramFrequenciesFeatureExtractor,
    word_ngram_counts: Counter[NGram],
) -> None:
    assert feature_extractor.word_ngram_counts() == word_ngram_counts


def test_all_word_ngrams_count(
    feature_extractor: AverageWordNgramFrequenciesFeatureExtractor,
    all_word_ngrams_count: int,
) -> None:
    assert feature_extractor.all_word_ngrams_count() == all_word_ngrams_count


def test_average_word_ngram_frequencies(
    feature: AverageWordNgramFrequenciesFeature,
    average_word_ngram_frequencies: dict[NGram, float],
) -> None:
    assert feature.average_word_ngram_frequencies() == approx(
        average_word_ngram_frequencies
    )
