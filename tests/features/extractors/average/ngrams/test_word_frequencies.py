from collections import Counter
from pytest import fixture

from authorship_attribution._internal.features.extractors.average.ngrams.character_frequencies import (
    CharacterNgramFrequenciesFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def text() -> Text:
    return "Hello... This is my life!"


@fixture
def ngram_size() -> int:
    return 2


@fixture
def extractor(text: Text, ngram_size: int) -> CharacterNgramFrequenciesFeatureExtractor:
    return CharacterNgramFrequenciesFeatureExtractor(text, ngram_size)


def ngram_counts(extractor: CharacterNgramFrequenciesFeatureExtractor) -> None:
    assert extractor.ngram_counts() == Counter[str]({"hello this": 1, "this is": 1, "is my": 1, "my life": 1})


def all_ngrams_count(extractor: CharacterNgramFrequenciesFeatureExtractor) -> None:
    assert extractor.all_ngrams_count() == 4