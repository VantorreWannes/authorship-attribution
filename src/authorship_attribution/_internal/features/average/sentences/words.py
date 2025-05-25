from authorship_attribution._internal.features.base.base import Feature


class AverageSentenceLengthInWordsFeature(Feature):
    def __init__(self, word_count: int, sentence_count: int) -> None:
        super().__init__()
        self.word_count = word_count
        self.sentence_count = sentence_count

    def average_sentence_length_in_words(self) -> float:
        if self.sentence_count == 0:
            return 0.0
        return self.word_count / self.sentence_count