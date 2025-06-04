from authorship_attribution._internal.features.extractors.base.words import (
    WordFeatureExtractor,
)
from authorship_attribution._internal.helpers import ngrams
from authorship_attribution._internal.types.aliases import Text


class WordNgramsFeatureExtractor(WordFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text)
        self.ngrams = ngrams(self.words, ngram_size)
