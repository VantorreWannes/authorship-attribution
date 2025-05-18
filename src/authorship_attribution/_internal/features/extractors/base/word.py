from nltk import word_tokenize
from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text, Word


class WordFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.words: list[Word] = word_tokenize(text)
