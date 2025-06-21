from collections import Counter
from typing import override
from authorship_attribution._internals.features.base import (
    Feature,
    WordNgramsFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import NGram, Text


class AverageWordNgramFrequenciesFeature(Feature):
    def __init__(
        self, word_ngram_counts: Counter[NGram], all_word_ngrams_count: int
    ) -> None:
        super().__init__()
        self.word_ngram_counts = word_ngram_counts
        self.all_word_ngrams_count = all_word_ngrams_count

    def average_word_ngram_frequencies(self) -> dict[NGram, float]:
        if self.all_word_ngrams_count == 0:
            return dict[NGram, float]()
        return {
            ngram: count / self.all_word_ngrams_count
            for ngram, count in self.word_ngram_counts.items()
        }
