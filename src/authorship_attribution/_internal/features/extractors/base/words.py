import string
from nltk import word_tokenize
from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text, Word


class WordFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        words_with_punctuation = word_tokenize(text)
        self.words: list[Word] = [
            word for word in words_with_punctuation if word not in string.punctuation
        ]
