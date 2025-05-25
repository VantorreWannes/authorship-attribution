from typing import override
from authorship_attribution._internal.features.average.words.lengths import (
    AverageWordLengthFeature,
)
from authorship_attribution._internal.features.extractors.base.words import (
    WordFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


class AverageWordLengthFeatureExtractor(WordFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)

    def word_count(self) -> int:
        return len(self.words)

    def summed_word_lengths(self) -> int:
        return sum(len(word) for word in self.words)

    @override
    def feature(self) -> AverageWordLengthFeature:
        word_count = self.word_count()
        summed_word_lengths = self.summed_word_lengths()
        return AverageWordLengthFeature(word_count, summed_word_lengths)
