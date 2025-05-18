from pytest import fixture
import pytest

from authorship_attribution._internal.features.average.word_length import (
    AverageWordLengthFeature,
)


@fixture
def word_count() -> int:
    return 100


@fixture
def summed_word_lengths() -> int:
    return 1000


@fixture
def average_word_length_feature(
    word_count: int, summed_word_lengths: int
) -> AverageWordLengthFeature:
    return AverageWordLengthFeature(word_count, summed_word_lengths)


def test_average_word_length(
    average_word_length_feature: AverageWordLengthFeature,
) -> None:
    assert average_word_length_feature.average_word_length() == pytest.approx(10.0)
