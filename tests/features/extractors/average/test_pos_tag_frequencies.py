from pytest import fixture

from authorship_attribution._internal.features.extractors.average.pos_tag_frequencies import (
    PartOfSpeechTagFrequenciesFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


@fixture
def text() -> Text:
    return "This is a test text. Don't take it seriously."

@fixture
def extractor(text: Text) -> PartOfSpeechTagFrequenciesFeatureExtractor:
    return PartOfSpeechTagFrequenciesFeatureExtractor(text)

def test_part_of_speach_tags_counts(extractor: PartOfSpeechTagFrequenciesFeatureExtractor):
    assert extractor.part_of_speach_tags_counts() == {'DT': 2, 'NN': 2, 'PRP': 1, 'RB': 2, 'VB': 1, 'VBP': 1, 'VBZ': 1}

def test_total_part_of_speach_tags_count(extractor: PartOfSpeechTagFrequenciesFeatureExtractor):
    assert extractor.total_part_of_speach_tags_count() == 10