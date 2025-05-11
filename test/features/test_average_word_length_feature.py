from pytest import fixture
import pytest

from authorship_attribution import Word, AverageWordLengthFeature


@fixture
def word_lengths() -> dict[Word, int]:
    return {"hello": 5, "world": 5, "this": 4, "is": 2, "a": 1, "test": 4}


@fixture
def average() -> float:
    return 3.5


@fixture
def feature(word_lengths) -> AverageWordLengthFeature:
    return AverageWordLengthFeature(word_lengths)


def test_average(feature: AverageWordLengthFeature, average: float):
    assert feature.average() == pytest.approx(average)
