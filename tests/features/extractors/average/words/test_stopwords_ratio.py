from pytest import fixture, approx

from authorship_attribution._internal.features.extractors.average.words.stopwords_ratio import (
    StopwordsRatioFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def text_with_stopwords() -> Text:
    return "This is a sample text and it contains some of the stopwords."


@fixture
def text_no_stopwords() -> Text:
    return "MyCorp lexicographers craft elegant prose."


@fixture
def text_empty() -> Text:
    return ""


@fixture
def extractor_with_stopwords(
    text_with_stopwords: Text,
) -> StopwordsRatioFeatureExtractor:
    return StopwordsRatioFeatureExtractor(text_with_stopwords)


@fixture
def extractor_no_stopwords(text_no_stopwords: Text) -> StopwordsRatioFeatureExtractor:
    return StopwordsRatioFeatureExtractor(text_no_stopwords)


@fixture
def extractor_empty(text_empty: Text) -> StopwordsRatioFeatureExtractor:
    return StopwordsRatioFeatureExtractor(text_empty)


def test_stopwords_count_with_stopwords(
    extractor_with_stopwords: StopwordsRatioFeatureExtractor,
) -> None:
    assert extractor_with_stopwords.stopwords_count() == 8


def test_total_word_count_with_stopwords(
    extractor_with_stopwords: StopwordsRatioFeatureExtractor,
) -> None:
    assert extractor_with_stopwords.total_word_count() == 13


def test_stopwords_count_no_stopwords(
    extractor_no_stopwords: StopwordsRatioFeatureExtractor,
) -> None:
    assert extractor_no_stopwords.stopwords_count() == 0


def test_total_word_count_no_stopwords(
    extractor_no_stopwords: StopwordsRatioFeatureExtractor,
) -> None:
    assert extractor_no_stopwords.total_word_count() == 6


def test_stopwords_count_empty(extractor_empty: StopwordsRatioFeatureExtractor) -> None:
    assert extractor_empty.stopwords_count() == 0


def test_total_word_count_empty(
    extractor_empty: StopwordsRatioFeatureExtractor,
) -> None:
    assert extractor_empty.total_word_count() == 0


def test_feature_extraction_with_stopwords(
    extractor_with_stopwords: StopwordsRatioFeatureExtractor,
) -> None:
    feature = extractor_with_stopwords.feature()
    assert feature.stopwords_count == 8
    assert feature.total_word_count == 13
    assert feature.stopwords_ratio() == approx(8 / 13)


def test_feature_extraction_no_stopwords(
    extractor_no_stopwords: StopwordsRatioFeatureExtractor,
) -> None:
    feature = extractor_no_stopwords.feature()
    assert feature.stopwords_count == 0
    assert feature.total_word_count == 6
    assert feature.stopwords_ratio() == approx(0.0)


def test_feature_extraction_empty(
    extractor_empty: StopwordsRatioFeatureExtractor,
) -> None:
    feature = extractor_empty.feature()
    assert feature.stopwords_count == 0
    assert feature.total_word_count == 0
    assert feature.stopwords_ratio() == approx(0.0)
