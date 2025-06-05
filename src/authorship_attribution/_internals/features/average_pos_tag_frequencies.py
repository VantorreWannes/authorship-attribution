from collections import Counter
from authorship_attribution._internals.features.base import Feature
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
