from authorship_attribution.__internal._data_types.type_aliases import Sentence
from authorship_attribution.__internal._features.primitive_feature import (
    PrimitiveFeature,
)


class AverageSentenceLengthFeature(PrimitiveFeature):
    def __init__(self, sentence_lengths: dict[Sentence, int]):
        super().__init__(sentence_lengths)

    def sentence_lengths(self) -> dict[Sentence, int]:
        return self.value

    def sentence_count(self) -> int:
        sentence_word_counts = self.sentence_lengths()
        return len(sentence_word_counts)

    def total_sentence_length(self) -> int:
        sentence_word_counts = self.sentence_lengths()
        return sum(sentence_word_counts.values())

    def average(self) -> float:
        return self.total_sentence_length() / self.sentence_count()


class AverageSentenceLengthInWordsFeature(AverageSentenceLengthFeature):
    def __init__(self, sentence_lengths: dict[Sentence, int]):
        super().__init__(sentence_lengths)


class AverageSentenceLengthInCharactersFeature(AverageSentenceLengthFeature):
    def __init__(self, sentence_lengths: dict[Sentence, int]):
        super().__init__(sentence_lengths)
