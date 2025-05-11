import pytest
from authorship_attribution import AverageWordLengthFeatureExtractor


@pytest.fixture
def words():
    return ["hello", "world", "this", "is", "a", "test"]


@pytest.fixture
def lengths() -> dict[str, int]:
    return {"hello": 5, "world": 5, "this": 4, "is": 2, "a": 1, "test": 4}


@pytest.fixture
def average() -> float:
    return 3.5


@pytest.fixture
def extractor(words):
    return AverageWordLengthFeatureExtractor(words)


def test_word_lengths(extractor: AverageWordLengthFeatureExtractor, lengths):
    word_lengths = extractor.word_lengths()
    assert word_lengths == lengths


def test_feature(extractor: AverageWordLengthFeatureExtractor, average):
    feature = extractor.feature()
    assert feature.average() == average
