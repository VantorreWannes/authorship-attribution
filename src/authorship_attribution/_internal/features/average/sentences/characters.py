from authorship_attribution._internal.features.base.base import Feature


class AverageSentenceLengthInCharactersFeature(Feature):
    def __init__(self, character_count: int, sentence_count: int) -> None:
        super().__init__()
        self.character_count = character_count
        self.sentence_count = sentence_count

    def average_sentence_length_in_characters(self) -> float:
        return self.character_count / self.sentence_count