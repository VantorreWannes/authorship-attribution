from collections import Counter
from typing import Literal
from pytest import fixture

from authorship_attribution._internal.features.average.pos_tag_frequencies import (
    PartOfSpeechTagFrequenciesFeature,
)
from authorship_attribution._internal.types.aliases import Json


@fixture
def name() -> Literal["part_of_speech_tag_frequencies_feature"]:
    return "part_of_speech_tag_frequencies_feature"


@fixture
def file_name() -> Literal["part_of_speech_tag_frequencies_feature.json"]:
    return "part_of_speech_tag_frequencies_feature.json"


@fixture
def part_of_speach_tags_counts() -> Counter[str]:
    return Counter[str]({"NN": 3, "VB": 5, "JJ": 2})


@fixture
def total_part_of_speach_tags_count() -> int:
    return 10


@fixture
def json(
    part_of_speach_tags_counts: Counter[str], total_part_of_speach_tags_count: int
) -> Json:
    return {
        "part_of_speach_tags_counts": part_of_speach_tags_counts,
        "total_part_of_speach_tags_count": total_part_of_speach_tags_count,
    }


@fixture
def feature(
    part_of_speach_tags_counts: Counter[str], total_part_of_speach_tags_count: int
) -> PartOfSpeechTagFrequenciesFeature:
    return PartOfSpeechTagFrequenciesFeature(
        part_of_speach_tags_counts,
        total_part_of_speach_tags_count,
    )


def test_name(name: Literal["part_of_speech_tag_frequencies_feature"]) -> None:
    assert PartOfSpeechTagFrequenciesFeature.name() == name


def test_file_name(
    file_name: Literal["part_of_speech_tag_frequencies_feature.json"],
) -> None:
    assert PartOfSpeechTagFrequenciesFeature.file_name() == file_name


def test_to_json(feature: PartOfSpeechTagFrequenciesFeature, json: Json) -> None:
    assert feature.to_json() == json


def test_from_json(
    json: Json,
    part_of_speach_tags_counts: dict[str, int],
    total_part_of_speach_tags_count: int,
) -> None:
    feature = PartOfSpeechTagFrequenciesFeature.from_json(data=json)
    assert isinstance(feature, PartOfSpeechTagFrequenciesFeature)
    assert feature.part_of_speach_tags_counts == part_of_speach_tags_counts
    assert feature.total_part_of_speach_tags_count == total_part_of_speach_tags_count
