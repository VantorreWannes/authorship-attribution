from authorship_attribution.__internal._data_types import Word
from authorship_attribution.__internal._features._extractors import (
    LexicalFeatureExtractor,
)


class WordFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, words: list[Word]):
        super().__init__()
        self.words: list[Word] = words
