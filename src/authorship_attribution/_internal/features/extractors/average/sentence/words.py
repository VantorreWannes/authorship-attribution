from nltk.tokenize import word_tokenize
from authorship_attribution._internal.features.extractors.base.sentence import (
    SentenceFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


class AverageSentenceLengthInWordsFeatureExtractor(SentenceFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)

    def word_count(self) -> int:
        return len(*[word_tokenize(sentence) for sentence in self.sentences])

    def sentence_count(self) -> int:
        return len(self.sentences)
