from pytest import fixture

from authorship_attribution import (
    Word,
    TypeTokenRatioFeatureExtractor,
)


@fixture
def words() -> list[Word]:
    return ["this", "world", "is", "this", "a", "test"]


@fixture
def word_count() -> int:
    return 6


@fixture
def unique_word_count() -> int:
    return 5


@fixture
def extractor(words: list[Word]) -> TypeTokenRatioFeatureExtractor:
    return TypeTokenRatioFeatureExtractor(words)


def test_feature(
    extractor: TypeTokenRatioFeatureExtractor, word_count: int, unique_word_count: int
):
    feature = extractor.feature()
    assert feature.word_count == word_count
    assert feature.unique_word_count == unique_word_count
