from typing import Counter, override

from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.features.average.character_frequencies import (
    CharacterFrequenciesFeature,
)
from authorship_attribution._internal.types.aliases import Text


class CharacterFrequenciesFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.normalised_text: Text = self.text.lower()

    def character_counts(self) -> Counter[str]:
        return Counter[str](self.normalised_text)

    def all_characters_count(self) -> int:
        return len(self.normalised_text)

    @override
    def feature(self) -> CharacterFrequenciesFeature:
        character_counts: Counter[str] = self.character_counts()
        all_characters_count: int = self.all_characters_count()
        return CharacterFrequenciesFeature(character_counts, all_characters_count)
