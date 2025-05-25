from authorship_attribution._internal.features.average.sentences.characters import (
    AverageSentenceLengthInCharactersFeature,
)


from typing import Literal
from pytest import fixture, approx

from authorship_attribution._internal.features.extractors.average.sentences.characters import (
    AverageSentenceLengthInCharactersFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def sample_text() -> Text:
    return "This is a test text. This is a second test text."


@fixture
def empty_text() -> Text:
    return ""


@fixture
def expected_character_count() -> int:
    return 20 + 27


@fixture
def expected_sentence_count() -> Literal[2]:
    return 2


@fixture
def extractor(
    sample_text: Text,
) -> AverageSentenceLengthInCharactersFeatureExtractor:  # Renamed
    return AverageSentenceLengthInCharactersFeatureExtractor(sample_text)


@fixture
def empty_extractor(
    empty_text: Text,
) -> AverageSentenceLengthInCharactersFeatureExtractor:
    return AverageSentenceLengthInCharactersFeatureExtractor(empty_text)


def test_character_count(
    extractor: AverageSentenceLengthInCharactersFeatureExtractor,
    expected_character_count: int,
) -> None:
    assert extractor.character_count() == expected_character_count


def test_sentence_count(
    extractor: AverageSentenceLengthInCharactersFeatureExtractor,
    expected_sentence_count: Literal[2],
) -> None:
    assert extractor.sentence_count() == expected_sentence_count


def test_feature_extraction(
    extractor: AverageSentenceLengthInCharactersFeatureExtractor,
    expected_character_count: int,
    expected_sentence_count: Literal[2],
) -> None:
    feature: AverageSentenceLengthInCharactersFeature = extractor.feature()
    assert feature.character_count == expected_character_count
    assert feature.sentence_count == expected_sentence_count
    assert feature.average_sentence_length_in_characters() == approx(
        expected_character_count / expected_sentence_count
    )


def test_empty_text_extraction(
    empty_extractor: AverageSentenceLengthInCharactersFeatureExtractor,
) -> None:
    assert empty_extractor.character_count() == 0
    assert empty_extractor.sentence_count() == 0
    feature: AverageSentenceLengthInCharactersFeature = empty_extractor.feature()
    assert feature.character_count == 0
    assert feature.sentence_count == 0
    assert feature.average_sentence_length_in_characters() == approx(0.0)
