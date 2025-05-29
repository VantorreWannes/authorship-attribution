import string
from typing import Counter
from authorship_attribution._internal.features.average.punctuation_frequencies import (
    PunctuationFrequenciesFeature,
)
from authorship_attribution._internal.features.extractors.base.lexical import (
    LexicalFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


class PunctuationFrequenciesFeatureExtractor(LexicalFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.punctuations = [char for char in self.text if char in string.punctuation]

    def punctuation_counts(self) -> Counter[str]:
        return Counter[str](self.punctuations)

    def total_punctuation_count(self) -> int:
        return len(self.punctuations)

    def feature(self) -> PunctuationFrequenciesFeature:
        punctuation_counts: Counter[str] = self.punctuation_counts()
        total_punctuation_count: int = self.total_punctuation_count()
        return PunctuationFrequenciesFeature(
            punctuation_counts, total_punctuation_count
        )
