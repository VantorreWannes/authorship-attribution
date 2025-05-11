from authorship_attribution.__internal._data_types.type_aliases import Word
from authorship_attribution.__internal._features._extractors.word_extractor import (
    WordFeatureExtractor,
)
from authorship_attribution.__internal._features.average_word_length_feature import (
    AverageWordLengthFeature,
)


class AverageWordLengthFeatureExtractor(WordFeatureExtractor):
    def __init__(self, words: list[Word]):
        super().__init__(words)

    @staticmethod
    def __word_length(word: str) -> int:
        return len(word)

    def _word_lengths(self) -> dict[Word, int]:
        return {
            word: AverageWordLengthFeatureExtractor.__word_length(word)
            for word in self.words
        }

    def feature(self) -> AverageWordLengthFeature:
        word_lengths = self._word_lengths()
        return AverageWordLengthFeature(word_lengths)
