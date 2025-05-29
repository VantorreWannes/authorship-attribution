from pytest import fixture

from authorship_attribution._internal.features.extractors.average.character_frequencies import (
    CharacterFrequenciesFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def sample_text() -> Text:
    return "ABBCCC...."


@fixture
def extractor(sample_text: Text) -> CharacterFrequenciesFeatureExtractor:
    return CharacterFrequenciesFeatureExtractor(sample_text)


def test_character_counts(extractor: CharacterFrequenciesFeatureExtractor) -> None:
    assert extractor.character_counts() == {"a": 1, "b": 2, "c": 3, '.': 4}


def test_all_characters_count(extractor: CharacterFrequenciesFeatureExtractor) -> None:
    assert extractor.all_characters_count() == 10
