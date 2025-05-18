from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Sentence, Text
from nltk import sent_tokenize


class SentenceFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.sentences: list[Sentence] = sent_tokenize(text)
