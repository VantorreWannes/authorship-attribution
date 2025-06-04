from collections import Counter
from pytest import fixture

from authorship_attribution._internal.features.average.ngrams.character_frequencies import (
    CharacterNgramFrequenciesFeature,
)
from authorship_attribution._internal.types.aliases import Json


@fixture
def name() -> str:
    return "character_ngram_frequencies_feature"


@fixture
def file_name() -> str:
    return "character_ngram_frequencies_feature.json"

@fixture
def ngram_counts() -> Counter[str]:
    return Counter({"hello": 3, "xD": 2, "oops": 1})

@fixture
def all_ngrams_count() -> int:
    return 5


@fixture
def json(ngram_counts: Counter[str], all_ngrams_count: int) -> Json:
    return {
        "ngram_counts": ngram_counts,
        "all_ngrams_count": all_ngrams_count,
    }


@fixture
def feature(
    ngram_counts: Counter[str], all_ngrams_count: int
) -> CharacterNgramFrequenciesFeature:
    return CharacterNgramFrequenciesFeature(
        ngram_counts,
        all_ngrams_count,
    )


def test_name(name: str) -> None:
    assert CharacterNgramFrequenciesFeature.name() == name


def test_file_name(file_name: str) -> None:
    assert CharacterNgramFrequenciesFeature.file_name() == file_name


def test_to_json(feature: CharacterNgramFrequenciesFeature, json: Json) -> None:
    assert feature.to_json() == json


def test_from_json(
    json: Json,
    ngram_counts: Counter[str],
    all_ngrams_count: int,
) -> None:
    feature = CharacterNgramFrequenciesFeature.from_json(data=json)
    assert isinstance(feature, CharacterNgramFrequenciesFeature)
    assert feature.ngram_counts == ngram_counts
    assert feature.all_ngrams_count == all_ngrams_count
