from authorship_attribution._internals.features.base import Feature


class AverageSentenceLengthInCharactersFeature(Feature):
    def __init__(self, summed_sentences_length: int, sentences_count: int) -> None:
        super().__init__()
        self.summed_sentences_length = summed_sentences_length
        self.sentences_count = sentences_count

    def average_sentence_length_in_characters(self) -> float:
        if self.sentences_count == 0:
            return 0.0
        return self.summed_sentences_length / self.sentences_count