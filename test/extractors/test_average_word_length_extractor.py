from pytest import fixture
from authorship_attribution import Word, AverageWordLengthFeatureExtractor


@fixture
def words() -> list[Word]:
    return ["hello", "world", "this", "is", "a", "test"]


@fixture
def word_lengths() -> dict[Word, int]:
    return {"hello": 5, "world": 5, "this": 4, "is": 2, "a": 1, "test": 4}


@fixture
def extractor(words) -> AverageWordLengthFeatureExtractor:
    return AverageWordLengthFeatureExtractor(words)


def test_feature(extractor: AverageWordLengthFeatureExtractor, word_lengths):
    assert extractor.feature().value == word_lengths
