from authorship_attribution.__internal._data_types.type_aliases import Sentence
from authorship_attribution.__internal._features._extractors.lexical_extrator import (
    LexicalFeatureExtractor,
)


class SentenceFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, sentences: list[Sentence]):
        super().__init__()
        self.sentences: list[Sentence] = sentences
