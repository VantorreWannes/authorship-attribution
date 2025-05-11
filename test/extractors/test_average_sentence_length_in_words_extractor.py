from pytest import fixture

from authorship_attribution import (
    Sentence,
    AverageSentenceLengthInWordsFeatureExtractor,
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
        "This is a test sentence.": 6,
        "This is another test sentence.": 6,
        "This is a third test sentence.": 7,
    }


@fixture
def extractor(sentences):
    return AverageSentenceLengthInWordsFeatureExtractor(sentences)


def test_feature(
    extractor: AverageSentenceLengthInWordsFeatureExtractor, sentence_lengths
):
    assert extractor.feature().value == sentence_lengths
