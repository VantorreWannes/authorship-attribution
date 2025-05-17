from pytest import fixture
import pytest

from authorship_attribution import TypeTokenRatioFeature


@fixture
def word_count() -> int:
    return 6


@fixture
def unique_word_count() -> int:
    return 3


@fixture
def type_token_ratio() -> float:
    return 0.5


@fixture
def feature(word_count, unique_word_count) -> TypeTokenRatioFeature:
    return TypeTokenRatioFeature(word_count, unique_word_count)


def test_type_token_ratio(feature: TypeTokenRatioFeature, type_token_ratio: float):
    assert feature.type_token_ratio() == pytest.approx(type_token_ratio)
