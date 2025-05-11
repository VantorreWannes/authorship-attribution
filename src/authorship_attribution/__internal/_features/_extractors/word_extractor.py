from authorship_attribution.__internal._data_types.type_aliases import Word
from authorship_attribution.__internal._features._extractors.lexical_extrator import (
    LexicalFeatureExtractor,
)


class WordFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, words: list[Word]):
        super().__init__()
        self.words: list[Word] = words
