from abc import ABC, abstractmethod
from authorship_attribution._internals.base_features import Feature
from authorship_attribution._internals.helpers import ngrams
from authorship_attribution._internals.types.aliases import Sentence, Text
from nltk import pos_tag, sent_tokenize, word_tokenize


class FeatureExtractor(ABC):
    @abstractmethod
    def feature(self) -> Feature:
        pass


class TextFeatureExtractor(FeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__()
        self.text: Text = text


class SentencesFeatureExtractor(TextFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.sentences: list[Sentence] = sent_tokenize(text)


class WordsFeatureExtractor(TextFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.words = word_tokenize(text)


class PosTagFeatureExtractor(WordsFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.part_of_speech_tags = [tag for _, tag in pos_tag(self.words)]


class CharacterNgramsFeatureExtractor(TextFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text)
        self.ngrams = ngrams(list[str](self.text), ngram_size)


class WordNgramsFeatureExtractor(WordsFeatureExtractor):
    def __init__(self, text: Text, ngram_size: int) -> None:
        super().__init__(text)
        self.ngrams = ngrams(self.words, ngram_size)
