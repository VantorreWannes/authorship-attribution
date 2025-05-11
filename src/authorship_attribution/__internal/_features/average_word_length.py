from authorship_attribution.__internal._data_types import Word
from authorship_attribution.__internal._features import PrimitiveFeature


class AverageWordLengthFeature(PrimitiveFeature):
    def __init__(self, word_lengths: dict[Word, int]):
        super().__init__(word_lengths)

    def average(self) -> float:
        word_lengths: dict[Word, int] = self.value
        return sum(word_lengths.values()) / len(self.value)
