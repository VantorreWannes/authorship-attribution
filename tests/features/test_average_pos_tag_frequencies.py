from collections import Counter
from pytest import approx, fixture

from authorship_attribution._internals.features.average_pos_tag_frequencies import (
    AveragePosTagFrequenciesFeature,
    AveragePosTagFrequenciesFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import PosTag


@fixture
def text() -> str:
    return "hello i am wannes"


@fixture
def pos_tag_counts() -> Counter[PosTag]:
    return Counter[PosTag]({"NN": 2, "NNS": 1, "VBP": 1})


@fixture
def all_pos_tags_count() -> int:
    return 4


@fixture
def average_pos_tag_frequencies() -> dict[PosTag, float]:
    return {"NN": 0.5, "NNS": 0.25, "VBP": 0.25}


@fixture
def feature(
    pos_tag_counts: Counter[PosTag], all_pos_tags_count: int
) -> AveragePosTagFrequenciesFeature:
    return AveragePosTagFrequenciesFeature(pos_tag_counts, all_pos_tags_count)


@fixture
def feature_extractor(text: str) -> AveragePosTagFrequenciesFeatureExtractor:
    return AveragePosTagFrequenciesFeatureExtractor(text)


def test_pos_tag_counts(
    feature_extractor: AveragePosTagFrequenciesFeatureExtractor,
    pos_tag_counts: Counter[PosTag],
) -> None:
    assert feature_extractor.pos_tag_counts() == pos_tag_counts


def test_all_postags_count(
    feature_extractor: AveragePosTagFrequenciesFeatureExtractor,
    all_pos_tags_count: int,
) -> None:
    assert feature_extractor.all_pos_tags_count() == all_pos_tags_count


def test_average_pos_tag_frequencies(
    feature: AveragePosTagFrequenciesFeature,
    average_pos_tag_frequencies: dict[PosTag, float],
) -> None:
    assert feature.average_pos_tag_frequencies() == approx(
        average_pos_tag_frequencies, abs=0.01
    )
