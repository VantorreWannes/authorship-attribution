from ..._feature_extractors import FeatureExtractor
from .average_length import AverageWordLengthExtractor, AverageWordLengthFeature, Average


type Sentence = str


type Word = str

class LexicalFeatureExtractor(FeatureExtractor):
    def __init__(self):
        super().__init__()


class WordFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, words: list[Word]):
        super().__init__()
        self.words: list[Word] = words


class SentenceFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, sentences: list[Sentence]):
        super().__init__()
        self.sentences: list[Sentence] = sentences


__all__ = ["AverageWordLengthExtractor", "AverageWordLengthFeature", "Average", "Word", "Sentence"]
