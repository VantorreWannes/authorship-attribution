from typing import Counter
from authorship_attribution._internal.features.base.base import Feature


class CharacterFrequenciesFeature(Feature):
    def __init__(
        self, character_counts: Counter[str], all_characters_count: int
    ) -> None:
        super().__init__()
        self.character_counts = character_counts
        self.all_characters_count = all_characters_count

    def character_frequencies(self) -> dict[str, float]:
        if self.all_characters_count == 0:
            return dict[str, float]()
        return {
            char: count / self.all_characters_count
            for char, count in self.character_counts.items()
        }
