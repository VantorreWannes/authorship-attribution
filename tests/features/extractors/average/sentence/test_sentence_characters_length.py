from typing import Literal


from authorship_attribution._internal.features.extractors.average.sentence.characters import (
    AverageSentenceLengthInCharactersFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text
from pytest import fixture


@fixture
def text() -> Text:
    return "This is a test text. This is a test text."


@fixture
def character_count() -> Literal[40]:
    return 40


@fixture
def sentence_count() -> Literal[2]:
    return 2


@fixture
def average_sentence_length_in_characters_feature_extractor(
    text: Text,
) -> AverageSentenceLengthInCharactersFeatureExtractor:
    return AverageSentenceLengthInCharactersFeatureExtractor(text)


def test_character_count(
    average_sentence_length_in_characters_feature_extractor: AverageSentenceLengthInCharactersFeatureExtractor,
    character_count: Literal[40],
) -> None:
    assert average_sentence_length_in_characters_feature_extractor.character_count() == character_count


def test_sentence_count(
    average_sentence_length_in_characters_feature_extractor: AverageSentenceLengthInCharactersFeatureExtractor,
    sentence_count: Literal[2],
) -> None:
    assert (
        average_sentence_length_in_characters_feature_extractor.sentence_count()
        == sentence_count
    )
