from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Word


class WordFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, words: list[Word]) -> None:
        super().__init__()
        self.words: list[Word] = words
