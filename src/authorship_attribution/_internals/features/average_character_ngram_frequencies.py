from collections import Counter
from typing import override
from authorship_attribution._internals.features.base import (
    CharacterNgramsFeatureExtractor,
    Feature,
)
from authorship_attribution._internals.types.aliases import NGram, Text


class AverageCharacterNgramFrequenciesFeature(Feature):
    def __init__(
        self, character_ngram_counts: Counter[NGram], all_character_ngrams_count: int
    ) -> None:
        super().__init__()
        self.character_ngram_counts = character_ngram_counts
        self.all_character_ngrams_count = all_character_ngrams_count

    def character_ngram_frequencies(self) -> dict[NGram, float]:
        if self.all_character_ngrams_count == 0:
            return dict[NGram, float]()
        return {
            char: count / self.all_character_ngrams_count
            for char, count in self.character_ngram_counts.items()
        }


class AverageCharacterNgramFrequenciesFeatureExtractor(CharacterNgramsFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text, ngram_size)

    def character_ngram_counts(self) -> Counter[NGram]:
        return Counter[NGram](self.ngrams)

    def all_character_ngrams_count(self) -> int:
        return len(self.ngrams)

    @override
    def feature(self) -> AverageCharacterNgramFrequenciesFeature:
        character_ngram_counts: Counter[NGram] = self.character_ngram_counts()
        all_character_ngrams_count: int = self.all_character_ngrams_count()
        return AverageCharacterNgramFrequenciesFeature(
            character_ngram_counts, all_character_ngrams_count
        )
