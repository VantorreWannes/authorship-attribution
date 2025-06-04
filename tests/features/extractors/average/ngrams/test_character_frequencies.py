from collections import Counter
from pytest import fixture

from authorship_attribution._internal.features.extractors.average.ngrams.character_frequencies import (
    CharacterNgramFrequenciesFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def text() -> Text:
    return "ABCD"


@fixture
def ngram_size() -> int:
    return 2


@fixture
def extractor(text: Text, ngram_size: int) -> CharacterNgramFrequenciesFeatureExtractor:
    return CharacterNgramFrequenciesFeatureExtractor(text, ngram_size)


def ngram_counts(extractor: CharacterNgramFrequenciesFeatureExtractor) -> None:
    assert extractor.ngram_counts() == Counter[str]({"ab": 3, "bc": 2, "cd": 1})


def all_ngrams_count(extractor: CharacterNgramFrequenciesFeatureExtractor) -> None:
    assert extractor.all_ngrams_count() == 5