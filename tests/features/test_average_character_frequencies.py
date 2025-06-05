from _pytest.python_api import ApproxBase


from collections import Counter
from pytest import approx, fixture

from authorship_attribution._internals.features.average_character_frequencies import (
    AverageCharacterFrequenciesFeature,
    AverageCharacterFrequenciesFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import Character


@fixture
def text() -> str:
    return "abbccc....     "


@fixture
def character_counts() -> Counter[Character]:
    return Counter[Character]({"a": 1, "b": 2, "c": 3, ".": 4, " ": 5})


@fixture
def all_characters_count() -> int:
    return 15


@fixture
def average_character_frequencies() -> dict[Character, float]:
    return {
        "a": 0.06,
        "b": 0.13,
        "c": 0.2,
        ".": 0.26,
        " ": 0.33,
    }


@fixture
def feature(
    character_counts: Counter[Character], all_characters_count: int
) -> AverageCharacterFrequenciesFeature:
    return AverageCharacterFrequenciesFeature(character_counts, all_characters_count)


@fixture
def feature_extractor(text: str) -> AverageCharacterFrequenciesFeatureExtractor:
    return AverageCharacterFrequenciesFeatureExtractor(text)


def test_character_counts(
    feature_extractor: AverageCharacterFrequenciesFeatureExtractor,
    character_counts: Counter[Character],
) -> None:
    assert feature_extractor.character_counts() == character_counts


def test_all_characters_count(
    feature_extractor: AverageCharacterFrequenciesFeatureExtractor,
    all_characters_count: int,
) -> None:
    assert feature_extractor.all_characters_count() == all_characters_count


def test_average_character_frequencies(
    feature: AverageCharacterFrequenciesFeature,
    average_character_frequencies: dict[Character, float],
) -> None:
    assert feature.average_character_frequencies() == approx(
        average_character_frequencies, abs=0.01
    )
