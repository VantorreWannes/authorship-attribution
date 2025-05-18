from authorship_attribution._internal.features.base.values import ValuesFeature


class AverageWordLengthFeature(ValuesFeature):
    def __init__(self, word_count: int, summed_word_lengths: int) -> None:
        super().__init__(__word_count=word_count, __summed_word_lengths=summed_word_lengths)

    def word_count(self) -> int:
        return getattr(self, "__word_count")

    def summed_word_lengths(self) -> int:
        return getattr(self, "__summed_word_lengths")

    def average_word_length(self) -> float:
        return self.summed_word_lengths() / self.word_count()
