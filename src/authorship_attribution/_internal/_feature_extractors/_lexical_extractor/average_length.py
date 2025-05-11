from ..._feature_extractors import PrimitiveValueFeature
from .._lexical_extractor import Word, WordFeatureExtractor

type Average = float

class AverageWordLengthFeature(PrimitiveValueFeature):
    def __init__(self, value: Average):
        super().__init__(value)
    
    @staticmethod
    def name() -> str:
        return "average_word_length"


class AverageWordLengthExtractor(WordFeatureExtractor):
    def __init__(self, words: list[Word]):
        super().__init__(words)
        self.word_lengths = self._word_lengths()

    @staticmethod
    def __word_length(word: str) -> float:
        return len(word)

    def _word_lengths(self) -> dict[Word, float]:
        return {
            word: AverageWordLengthExtractor.__word_length(word) for word in self.words
        }

    def _summed_word_lengths(self) -> int:
        return sum(value for value in self._word_lengths().values())

    def average_word_length(self) -> Average:
        return self._summed_word_lengths() / len(self._word_lengths())

    def feature(self) -> AverageWordLengthFeature:
        return self.average_word_length()
