from authorship_attribution.__internal._data_types.type_aliases import Word
from authorship_attribution.__internal._features.primitive_feature import (
    PrimitiveFeature,
)


class AverageWordLengthFeature(PrimitiveFeature):
    def __init__(self, word_lengths: dict[Word, int]):
        super().__init__(word_lengths)

    def word_lengths(self) -> dict[Word, int]:
        return self.value

    def word_count(self) -> int:
        word_lengths = self.word_lengths()
        return len(word_lengths)

    def total_words_length(self) -> int:
        word_lengths = self.word_lengths()
        return sum(word_lengths.values())

    def average(self) -> float:
        return self.total_words_length() / self.word_count()
