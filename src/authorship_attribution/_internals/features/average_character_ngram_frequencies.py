from collections import Counter
from authorship_attribution._internals.features.base import Feature
from authorship_attribution._internals.types.aliases import NGram


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
