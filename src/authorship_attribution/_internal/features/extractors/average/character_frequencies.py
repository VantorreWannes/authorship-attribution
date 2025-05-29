import string
from typing import override

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

    def character_counts(self) -> dict[str, int]:
        text = self.text.lower()
        return {
            char: text.count(char) for char in text if char not in string.punctuation
        }

    def all_characters_count(self) -> int:
        text = self.text.lower()
        return len([char for char in text if char not in string.punctuation])

    @override
    def feature(self) -> CharacterFrequenciesFeature:
        character_counts: dict[str, int] = self.character_counts()
        all_characters_count: int = self.all_characters_count()
        return CharacterFrequenciesFeature(character_counts, all_characters_count)
