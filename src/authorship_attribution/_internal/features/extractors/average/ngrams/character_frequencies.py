from collections import Counter
from typing import override
from authorship_attribution._internal.features.average.ngrams.character_frequencies import (
    CharacterNgramFrequenciesFeature,
)
from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.helpers import ngrams
from authorship_attribution._internal.types.aliases import Text


class CharacterNgramFrequenciesFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text)
        self.ngrams = ngrams([char for char in text], ngram_size)

    def ngram_counts(self) -> Counter[str]:
        return Counter[str](self.ngrams)

    def all_ngrams_count(self) -> int:
        return len(self.ngrams)

    @override
    def feature(self) -> CharacterNgramFrequenciesFeature:
        ngram_counts: Counter[str] = self.ngram_counts()
        all_ngrams_count: int = self.all_ngrams_count()
        return CharacterNgramFrequenciesFeature(ngram_counts, all_ngrams_count)
