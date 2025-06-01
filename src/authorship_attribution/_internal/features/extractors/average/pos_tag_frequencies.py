from collections import Counter
from authorship_attribution._internal.features.average.pos_tag_frequencies import (
    PartOfSpeechTagFrequenciesFeature,
)
from authorship_attribution._internal.features.extractors.base.pos_tags import (
    PartOfSpeechTagFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


class PartOfSpeechTagFrequenciesFeatureExtractor(PartOfSpeechTagFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)

    def part_of_speach_tags_counts(self) -> Counter[str]:
        return Counter[str](self.part_of_speech_tags)

    def total_part_of_speach_tags_count(self) -> int:
        return len(self.part_of_speech_tags)

    def feature(self) -> PartOfSpeechTagFrequenciesFeature:
        part_of_speach_tags_counts: Counter[str] = self.part_of_speach_tags_counts()
        total_part_of_speach_tags_count: int = self.total_part_of_speach_tags_count()
        return PartOfSpeechTagFrequenciesFeature(
            part_of_speach_tags_counts, total_part_of_speach_tags_count
        )
