from pytest import fixture

from authorship_attribution import (
    Sentence,
    AverageSentenceLengthInCharactersFeatureExtractor,
)


@fixture
def sentences() -> list[Sentence]:
    return [
        "This is a test sentence.",
        "This is another test sentence.",
        "This is a third test sentence.",
    ]


@fixture
def sentence_lengths() -> dict[Sentence, int]:
    return {
        "This is a test sentence.": 24,
        "This is another test sentence.": 30,
        "This is a third test sentence.": 30,
    }


@fixture
def extractor(sentences):
    return AverageSentenceLengthInCharactersFeatureExtractor(sentences)


def test_feature(
    extractor: AverageSentenceLengthInCharactersFeatureExtractor, sentence_lengths
):
    assert extractor.feature().value == sentence_lengths
