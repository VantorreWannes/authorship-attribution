from typing import Any, Literal
from pytest import fixture
from authorship_attribution._internal.features.average.sentence.characters import (
    AverageSentenceLengthInCharactersFeature,
)


@fixture
def name() -> Literal["average_sentence_length_in_characters_feature"]:
    return "average_sentence_length_in_characters_feature"


@fixture
def file_name() -> Literal["average_sentence_length_in_characters_feature.json"]:
    return "average_sentence_length_in_characters_feature.json"


@fixture
def character_count() -> int:
    return 100


@fixture
def sentence_count() -> int:
    return 1000


@fixture
def json(character_count: int, sentence_count: int) -> dict[Any, Any]:
    return {"character_count": character_count, "sentence_count": sentence_count}


@fixture
def average_character_length_feature(
    character_count: int, sentence_count: int
) -> AverageSentenceLengthInCharactersFeature:
    return AverageSentenceLengthInCharactersFeature(character_count, sentence_count)


def test_name(name: Literal["average_sentence_length_in_characters_feature"]) -> None:
    assert AverageSentenceLengthInCharactersFeature.name() == name


def test_file_name(file_name: Literal["average_sentence_length_in_characters_feature.json"]) -> None:
    assert AverageSentenceLengthInCharactersFeature.file_name() == file_name


def test_to_json(
    average_character_length_feature: AverageSentenceLengthInCharactersFeature, json
) -> None:
    assert average_character_length_feature.to_json() == json


def test_from_json(json) -> None:
    assert AverageSentenceLengthInCharactersFeature.from_json(json)
