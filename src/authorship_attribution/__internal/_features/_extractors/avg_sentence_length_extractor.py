from abc import abstractmethod
from nltk import word_tokenize
from authorship_attribution.__internal._features._extractors.sentence_extractor import (
    SentenceFeatureExtractor,
)
from authorship_attribution.__internal._data_types.type_aliases import Sentence
from authorship_attribution.__internal._features.average_sentence_length_feature import (
    AverageSentenceLengthFeature,
)


class AverageSentenceLengthFeatureExtractor(SentenceFeatureExtractor):
    def __init__(self, sentences: list[Sentence]):
        super().__init__(sentences)

    @staticmethod
    @abstractmethod
    def _sentence_length(sentence: Sentence) -> int:
        pass

    def _sentence_lengths(self) -> dict[Sentence, int]:
        return {
            sentence: self._sentence_length(sentence) for sentence in self.sentences
        }

    def feature(self) -> AverageSentenceLengthFeature:
        return AverageSentenceLengthFeature(self._sentence_lengths())


class AverageSentenceLengthInWordsFeatureExtractor(
    AverageSentenceLengthFeatureExtractor
):
    @staticmethod
    def _sentence_length(sentence: Sentence) -> int:
        return len(word_tokenize(sentence))


class AverageSentenceLengthInCharactersFeatureExtractor(
    AverageSentenceLengthFeatureExtractor
):
    @staticmethod
    def _sentence_length(sentence: Sentence) -> int:
        return len(sentence)
