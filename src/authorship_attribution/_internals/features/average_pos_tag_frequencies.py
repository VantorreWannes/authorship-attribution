from collections import Counter
from typing import override
from authorship_attribution._internals.features.base import Feature, PosTagFeatureExtractor
from authorship_attribution._internals.types.aliases import PosTag


class AveragePosTagFrequenciesFeature(Feature):
    def __init__(self, pos_tag_counts: Counter[PosTag], all_pos_tag_count: int) -> None:
        super().__init__()
        self.pos_tag_counts = pos_tag_counts
        self.all_pos_tag_count = all_pos_tag_count

    def average_pos_tag_frequencies(self) -> dict[PosTag, float]:
        if self.all_pos_tag_count == 0:
            return dict[PosTag, float]()
        return {
            char: count / self.all_pos_tag_count
            for char, count in self.pos_tag_counts.items()
        }


class AveragePosTagFrequenciesFeatureExtractor(PosTagFeatureExtractor):
    def pos_tag_counts(self) -> Counter[PosTag]:
        return Counter[PosTag](self.pos_tags)

    def all_pos_tag_count(self) -> int:
        return len(self.pos_tags)

    @override
    def feature(self) -> AveragePosTagFrequenciesFeature:
        character_counts: Counter[PosTag] = self.pos_tag_counts()
        all_characters_count: int = self.all_pos_tag_count()
        return AveragePosTagFrequenciesFeature(
            character_counts, all_characters_count
        )
