import nltk
from authorship_attribution._internal.features.extractors.base.words import (
    WordFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


class PartOfSpeechTagFeatureExtractor(WordFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.part_of_speech_tags = [tag for _, tag in nltk.pos_tag(self.words)]
