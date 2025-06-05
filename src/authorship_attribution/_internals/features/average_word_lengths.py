from authorship_attribution._internals.features.base import Feature


class AverageWordLengthFeature(Feature):
    def __init__(self, summed_word_lengths: int, words_count: int) -> None:
        super().__init__()
        self.summed_word_lengths = summed_word_lengths
        self.words_count = words_count

    def average_word_length(self) -> float:
        if self.words_count == 0:
            return 0.0
        return self.summed_word_lengths / self.words_count
