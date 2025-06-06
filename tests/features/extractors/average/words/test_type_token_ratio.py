from typing import Literal
from pytest import fixture

from authorship_attribution._internal.features.extractors.average.words.type_token_ratio import (
    TypeTokenRatioFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def sample_text() -> Text:
    return "He he ha ha. Test test."


@fixture
def empty_text() -> Text:
    return ""


@fixture
def extractor(sample_text: Text) -> TypeTokenRatioFeatureExtractor:
    return TypeTokenRatioFeatureExtractor(text=sample_text)


@fixture
def empty_extractor(empty_text: Text) -> TypeTokenRatioFeatureExtractor:
    return TypeTokenRatioFeatureExtractor(text=empty_text)


@fixture
def expected_unique_words_count() -> Literal[3]:
    return 3


@fixture
def expected_all_words_count() -> Literal[6]:
    return 6


def test_unique_words_count(
    extractor: TypeTokenRatioFeatureExtractor,
    expected_unique_words_count: int,
) -> None:
    assert extractor.unique_words_count() == expected_unique_words_count


def test_all_words_count(
    extractor: TypeTokenRatioFeatureExtractor,
    expected_all_words_count: int,
) -> None:
    assert extractor.all_words_count() == expected_all_words_count
