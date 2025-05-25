from authorship_attribution._internal.features.base.base import Feature


class AverageWordLengthFeature(Feature):
    def __init__(self, word_count: int, summed_word_lengths: int) -> None:
        super().__init__()
        self.word_count = word_count
        self.summed_word_lengths = summed_word_lengths

    def average_word_length(self) -> float:
        if self.word_count == 0:
            return 0.0
        return self.summed_word_lengths / self.word_count