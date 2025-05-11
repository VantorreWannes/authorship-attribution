from authorship_attribution.__internal._data_types import Word
from authorship_attribution.__internal._features._extractors import WordFeatureExtractor
from authorship_attribution.__internal._features import AverageWordLengthFeature


class AverageWordLengthFeatureExtractor(WordFeatureExtractor):
    def __init__(self, words: list[Word]):
        super().__init__(words)

    @staticmethod
    def __word_length(word: str) -> float:
        return len(word)

    def word_lengths(self) -> dict[Word, float]:
        return {
            word: AverageWordLengthFeatureExtractor.__word_length(word)
            for word in self.words
        }

    def feature(self) -> AverageWordLengthFeature:
        word_lengths = self.word_lengths()
        return AverageWordLengthFeature(word_lengths)
