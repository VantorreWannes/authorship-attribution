from collections import Counter
from authorship_attribution._internal.features.average.ngrams.frequencies import NgramFrequenciesFeature


class CharacterNgramFrequenciesFeature(NgramFrequenciesFeature):
    def __init__(self, ngram_counts: Counter[str], all_ngrams_count: int) -> None:
        super().__init__(ngram_counts, all_ngrams_count)

    