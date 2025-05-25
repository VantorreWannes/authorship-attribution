from authorship_attribution._internal.features.average.sentences.characters import (
    AverageSentenceLengthInCharactersFeature,
)
from authorship_attribution._internal.features.extractors.base.sentences import (
    SentenceFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


class AverageSentenceLengthInCharactersFeatureExtractor(SentenceFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)

    def character_count(self) -> int:
        return sum(len(sentence) for sentence in self.sentences)

    def sentence_count(self) -> int:
        return len(self.sentences)

    def feature(self) -> AverageSentenceLengthInCharactersFeature:
        character_count = self.character_count()
        sentence_count = self.sentence_count()
        return AverageSentenceLengthInCharactersFeature(character_count, sentence_count)
