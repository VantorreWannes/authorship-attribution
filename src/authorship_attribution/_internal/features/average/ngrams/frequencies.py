from collections import Counter
from authorship_attribution._internal.features.base.base import Feature


class NgramFrequenciesFeature(Feature):

    def __init__(self, ngram_counts: Counter[str], all_ngrams_count: int) -> None:
        super().__init__()
        self.ngram_counts: Counter[str] = ngram_counts
        self.all_ngrams_count: int = all_ngrams_count

    def ngram_frequencies(self) -> dict[str, float]:
        if self.all_ngrams_count == 0:
            return dict[str, float]()
        return {
            char: count / self.all_ngrams_count
            for char, count in self.ngram_counts.items()
        }
