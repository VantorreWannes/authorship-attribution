from authorship_attribution._internal.features.average.words.type_token_ratio import (
    TypeTokenRatioFeature,
)


from typing import Literal
from pytest import fixture, approx

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
def expected_unique_words_count() -> Literal[4]:
    return 4


@fixture
def expected_all_words_count() -> Literal[8]:
    return 8


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


def test_feature_extraction(
    extractor: TypeTokenRatioFeatureExtractor,
    expected_unique_words_count: int,
    expected_all_words_count: int,
) -> None:
    feature: TypeTokenRatioFeature = extractor.feature()
    assert feature.unique_words_count == expected_unique_words_count
    assert feature.all_words_count == expected_all_words_count
    assert feature.type_token_ratio() == approx(
        expected=expected_unique_words_count / expected_all_words_count
    )


def test_empty_text_extraction(empty_extractor: TypeTokenRatioFeatureExtractor) -> None:
    assert empty_extractor.unique_words_count() == 0
    assert empty_extractor.all_words_count() == 0
    feature: TypeTokenRatioFeature = empty_extractor.feature()
    assert feature.unique_words_count == 0
    assert feature.all_words_count == 0
    assert feature.type_token_ratio() == approx(0.0)
