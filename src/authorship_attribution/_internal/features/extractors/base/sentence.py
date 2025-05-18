from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Sentence


class SentenceFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, sentence: list[Sentence]) -> None:
        super().__init__()
        self.sentence: list[Sentence] = sentence
