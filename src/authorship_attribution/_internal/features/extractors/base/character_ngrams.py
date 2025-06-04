from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.helpers import ngrams
from authorship_attribution._internal.types.aliases import Text


class CharacterNgramsFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text)
        self.ngrams = ngrams([char for char in text], ngram_size)
