from typing import Literal
from pytest import fixture

from authorship_attribution._internal.features.average.frequencies import (
    CharacterFrequenciesFeature,
)
from authorship_attribution._internal.types.aliases import Json


@fixture
def name() -> Literal["character_frequencies_feature"]:
    return "character_frequencies_feature"


@fixture
def file_name() -> Literal["character_frequencies_feature.json"]:
    return "character_frequencies_feature.json"


@fixture
def sample_character_counts() -> dict[str, int]:
    return {"a": 1, "b": 2, "c": 3}


@fixture
def sample_all_characters_count() -> int:
    return 6


@fixture
def json_data(
    sample_character_counts: dict[str, int], sample_all_characters_count: int
) -> Json:
    return {
        "character_counts": sample_character_counts,
        "all_characters_count": sample_all_characters_count,
    }


@fixture
def feature_instance(
    sample_character_counts: dict[str, int], sample_all_characters_count: int
) -> CharacterFrequenciesFeature:
    return CharacterFrequenciesFeature(
        character_counts=sample_character_counts,
        all_characters_count=sample_all_characters_count,
    )


def test_name(name: Literal["character_frequencies_feature"]) -> None:
    assert CharacterFrequenciesFeature.name() == name


def test_file_name(file_name: Literal["character_frequencies_feature.json"]) -> None:
    assert CharacterFrequenciesFeature.file_name() == file_name


def test_to_json(
    feature_instance: CharacterFrequenciesFeature, json_data: Json
) -> None:
    assert feature_instance.to_json() == json_data


def test_from_json(
    json_data: Json,
    sample_character_counts: dict[str, int],
    sample_all_characters_count: int,
) -> None:
    feature = CharacterFrequenciesFeature.from_json(json_data)
    assert isinstance(feature, CharacterFrequenciesFeature)
    assert feature.character_counts == sample_character_counts
    assert feature.all_characters_count == sample_all_characters_count
