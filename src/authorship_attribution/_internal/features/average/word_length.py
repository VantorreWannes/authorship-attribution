from authorship_attribution._internal.features.base.values import ValuesFeature


class AverageWordLengthFeature(ValuesFeature):
    def __init__(self, word_count: int, summed_word_lengths: int) -> None:
        super().__init__(word_count=word_count, summed_word_lengths=summed_word_lengths)
        self.word_count = self._get("word_count")
        self.summed_word_lengths = self._get("summed_word_lengths")

    def average_word_length(self) -> float:
        return self.summed_word_lengths / self.word_count
