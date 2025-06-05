from collections import Counter
from typing import override
from authorship_attribution._internals.features.base import (
    CharactersFeatureExtractor,
    Feature,
)
from authorship_attribution._internals.types.aliases import Character


class AverageCharacterFrequenciesFeature(Feature):
    def __init__(
        self, character_counts: Counter[Character], all_characters_count: int
    ) -> None:
        super().__init__()
        self.character_counts = character_counts
        self.all_characters_count = all_characters_count

    def average_character_frequencies(self) -> dict[str, float]:
        if self.all_characters_count == 0:
            return dict[str, float]()
        return {
            char: count / self.all_characters_count
            for char, count in self.character_counts.items()
        }


class AverageCharacterFrequenciesFeatureExtractor(CharactersFeatureExtractor):
    def character_counts(self) -> Counter[Character]:
        return Counter[Character](self.characters)

    def all_characters_count(self) -> int:
        return len(self.characters)

    @override
    def feature(self) -> AverageCharacterFrequenciesFeature:
        character_counts = self.character_counts()
        all_characters_count = self.all_characters_count()
        return AverageCharacterFrequenciesFeature(
            character_counts, all_characters_count
        )
