import string
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

    def punctuation_counts(self) -> dict[str, int]:
        return {
            char: self.text.count(char)
            for char in set[str](self.text)
            if char in string.punctuation
        }

    def total_punctuation_count(self) -> int:
        return len([char for char in self.text if char in string.punctuation])

    def feature(self) -> PunctuationFrequenciesFeature:
        punctuation_counts: dict[str, int] = self.punctuation_counts()
        total_punctuation_count: int = self.total_punctuation_count()
        return PunctuationFrequenciesFeature(
            punctuation_counts, total_punctuation_count
        )
