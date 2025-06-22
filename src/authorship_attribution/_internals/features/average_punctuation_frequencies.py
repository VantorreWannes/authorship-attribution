from collections import Counter
from typing import override
from authorship_attribution._internals.features.base import (
    Feature,
    PunctuationsFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import Punctuation


class AveragePunctuationFrequenciesFeature(Feature):
    def __init__(
        self, punctuation_counts: Counter[Punctuation], all_punctuations_count: int
    ) -> None:
        super().__init__()
        self.punctuation_counts = punctuation_counts
        self.all_punctuations_count = all_punctuations_count

    def average_pos_tag_frequencies(self) -> dict[Punctuation, float]:
        if self.all_punctuations_count == 0:
            return dict[Punctuation, float]()
        return {
            char: count / self.all_punctuations_count
            for char, count in self.punctuation_counts.items()
        }


class AveragePunctuationFrequenciesFeatureExtractor(PunctuationsFeatureExtractor):
    def punctuation_counts(self) -> Counter[Punctuation]:
        return Counter[Punctuation](self.punctuations)

    def all_punctuations_count(self) -> int:
        return len(self.punctuations)

    @override
    def feature(self) -> AveragePunctuationFrequenciesFeature:
        punctuation_counts: Counter[Punctuation] = self.punctuation_counts()
        all_punctuations_count: int = self.all_punctuations_count()
        return AveragePunctuationFrequenciesFeature(
            punctuation_counts, all_punctuations_count
        )
