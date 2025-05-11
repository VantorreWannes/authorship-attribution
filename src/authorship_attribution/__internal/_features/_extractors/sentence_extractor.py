from authorship_attribution.__internal._data_types import Sentence
from authorship_attribution.__internal._features._extractors import (
    LexicalFeatureExtractor,
)


class SentenceFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, sentences: list[Sentence]):
        super().__init__()
        self.sentences: list[Sentence] = sentences
