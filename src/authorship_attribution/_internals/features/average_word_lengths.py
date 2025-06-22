from authorship_attribution._internals.features.base import (
    Feature,
    WordsFeatureExtractor,
)


class AverageWordLengthFeature(Feature):
    def __init__(self, summed_word_lengths: int, words_count: int) -> None:
        super().__init__()
        self.summed_word_lengths = summed_word_lengths
        self.words_count = words_count

    def average_word_length(self) -> float:
        if self.words_count == 0:
            return 0.0
        return self.summed_word_lengths / self.words_count


class AverageWordLengthFeatureExtractor(WordsFeatureExtractor):
    def summed_word_lengths(self) -> int:
        return sum(len(word) for word in self.words)

    def words_count(self) -> int:
        return len(self.words)

    def feature(self) -> AverageWordLengthFeature:
        summed_word_lengths: int = self.summed_word_lengths()
        words_count: int = self.words_count()
        return AverageWordLengthFeature(summed_word_lengths, words_count)
