from typing import Counter, Literal
from pytest import fixture

from authorship_attribution._internal.features.average.punctuation_frequencies import (
    PunctuationFrequenciesFeature,
)
from authorship_attribution._internal.types.aliases import Json


@fixture
def name() -> Literal["punctuation_frequencies_feature"]:
    return "punctuation_frequencies_feature"


@fixture
def file_name() -> Literal["punctuation_frequencies_feature.json"]:
    return "punctuation_frequencies_feature.json"


@fixture
def sample_punctuation_counts() -> Counter[str]:
    return Counter[str]({".": 1, ",": 2, ";": 3})


@fixture
def sample_total_punctuation_count() -> int:
    return 6


@fixture
def json_data(
    sample_punctuation_counts: Counter[str], sample_total_punctuation_count: int
) -> Json:
    return {
        "punctuation_counts": sample_punctuation_counts,
        "total_punctuation_count": sample_total_punctuation_count,
    }


@fixture
def feature_instance(
    sample_punctuation_counts: Counter[str], sample_total_punctuation_count: int
) -> PunctuationFrequenciesFeature:
    return PunctuationFrequenciesFeature(
        punctuation_counts=sample_punctuation_counts,
        total_punctuation_count=sample_total_punctuation_count,
    )


def test_name(name: Literal["punctuation_frequencies_feature"]) -> None:
    assert PunctuationFrequenciesFeature.name() == name


def test_file_name(file_name: Literal["punctuation_frequencies_feature.json"]) -> None:
    assert PunctuationFrequenciesFeature.file_name() == file_name


def test_to_json(
    feature_instance: PunctuationFrequenciesFeature, json_data: Json
) -> None:
    assert feature_instance.to_json() == json_data


def test_from_json(
    json_data: Json,
    sample_punctuation_counts: dict[str, int],
    sample_total_punctuation_count: int,
) -> None:
    feature = PunctuationFrequenciesFeature.from_json(data=json_data)
    assert isinstance(feature, PunctuationFrequenciesFeature)
    assert feature.punctuation_counts == sample_punctuation_counts
    assert feature.total_punctuation_count == sample_total_punctuation_count
