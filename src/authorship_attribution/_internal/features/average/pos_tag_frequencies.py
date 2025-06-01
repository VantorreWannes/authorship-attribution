from typing import Counter
from authorship_attribution._internal.features.base.base import Feature


class PartOfSpeechTagFrequenciesFeature(Feature):
    pass

    def __init__(
        self,
        part_of_speach_tags_counts: Counter[str],
        total_part_of_speach_tags_count: int,
    ) -> None:
        super().__init__()
        self.part_of_speach_tags_counts = part_of_speach_tags_counts
        self.total_part_of_speach_tags_count = total_part_of_speach_tags_count

    def part_of_speach_tag_frequencies(self) -> dict[str, float]:
        if self.total_part_of_speach_tags_count == 0:
            return dict[str, float]()
        return {
            tag: count / self.total_part_of_speach_tags_count
            for tag, count in self.part_of_speach_tags_counts.items()
        }
