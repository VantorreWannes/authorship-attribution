from typing import Literal


from authorship_attribution._internal.features.extractors.average.words.type_token_ratio import (
    TypeTokenRatioFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text
from pytest import fixture


@fixture
def text() -> Text:
    return "He he ha ha"


@fixture
def type_token_ratio_feature_extractor(
    text: Text,
) -> TypeTokenRatioFeatureExtractor:
    return TypeTokenRatioFeatureExtractor(text)


@fixture
def unique_words_count() -> Literal[2]:
    return 2


@fixture
def all_words_count() -> Literal[4]:
    return 4


def test_unique_words_count(
    type_token_ratio_feature_extractor: TypeTokenRatioFeatureExtractor,
    unique_words_count: int,
) -> None:
    assert type_token_ratio_feature_extractor.unique_words_count() == unique_words_count


def test_all_words_count(
    type_token_ratio_feature_extractor: TypeTokenRatioFeatureExtractor,
    all_words_count: int,
) -> None:
    assert type_token_ratio_feature_extractor.all_words_count() == all_words_count
