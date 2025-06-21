from pytest import approx, fixture

from authorship_attribution._internals.features.average_sentence_length_in_characters import (
    AverageSentenceLengthInCharactersFeature,
    AverageSentenceLengthInCharactersFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import Text


@fixture
def text() -> str:
    return "Hello world, how are you? I'm good thanks!"


@fixture
def summed_sentences_length() -> int:
    return 41


@fixture
def sentences_count() -> int:
    return 2


@fixture
def average_sentence_length_in_characters() -> float:
    return 20.5


@fixture
def feature(
    summed_sentences_length: int, sentences_count: int
) -> AverageSentenceLengthInCharactersFeature:
    return AverageSentenceLengthInCharactersFeature(
        summed_sentences_length, sentences_count
    )


@fixture
def feature_extractor(text: Text) -> AverageSentenceLengthInCharactersFeatureExtractor:
    return AverageSentenceLengthInCharactersFeatureExtractor(text)


def test_summed_sentences_length(
    feature_extractor: AverageSentenceLengthInCharactersFeatureExtractor,
    summed_sentences_length: int,
) -> None:
    assert feature_extractor.summed_sentences_length() == summed_sentences_length


def test_sentences_count(
    feature_extractor: AverageSentenceLengthInCharactersFeatureExtractor,
    sentences_count: int,
) -> None:
    assert feature_extractor.sentences_count() == sentences_count


def test_average_sentence_length_in_characters(
    feature: AverageSentenceLengthInCharactersFeature,
    average_sentence_length_in_characters: float,
) -> None:
    assert feature.average_sentence_length_in_characters() == approx(
        average_sentence_length_in_characters
    )