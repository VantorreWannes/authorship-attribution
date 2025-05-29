from typing import Literal
from pytest import fixture, approx
from authorship_attribution._internal.features.average.sentences.characters import (
    AverageSentenceLengthInCharactersFeature,
)
from authorship_attribution._internal.types.aliases import Json


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
    return 10


@fixture
def json_data(character_count: int, sentence_count: int) -> Json:
    return {"character_count": character_count, "sentence_count": sentence_count}


@fixture
def average_character_length_feature(
    character_count: int, sentence_count: int
) -> AverageSentenceLengthInCharactersFeature:
    return AverageSentenceLengthInCharactersFeature(character_count, sentence_count)


def test_name(name: Literal["average_sentence_length_in_characters_feature"]) -> None:
    assert AverageSentenceLengthInCharactersFeature.name() == name


def test_file_name(
    file_name: Literal["average_sentence_length_in_characters_feature.json"],
) -> None:
    assert AverageSentenceLengthInCharactersFeature.file_name() == file_name


def test_to_json(
    average_character_length_feature: AverageSentenceLengthInCharactersFeature,
    json_data: Json,
) -> None:
    assert average_character_length_feature.to_json() == json_data


def test_from_json(json_data: Json, character_count: int, sentence_count: int) -> None:
    feature = AverageSentenceLengthInCharactersFeature.from_json(json_data)
    assert isinstance(feature, AverageSentenceLengthInCharactersFeature)
    assert feature.character_count == character_count
    assert feature.sentence_count == sentence_count


def test_average_calculation(
    average_character_length_feature: AverageSentenceLengthInCharactersFeature,
) -> None:
    assert (
        average_character_length_feature.average_sentence_length_in_characters()
        == approx(10.0)
    )


def test_average_calculation_zero_sentences() -> None:
    feature = AverageSentenceLengthInCharactersFeature(
        character_count=0, sentence_count=0
    )
    assert feature.average_sentence_length_in_characters() == approx(0.0)

    feature_with_chars = AverageSentenceLengthInCharactersFeature(
        character_count=50, sentence_count=0
    )
    assert feature_with_chars.average_sentence_length_in_characters() == approx(0.0)
