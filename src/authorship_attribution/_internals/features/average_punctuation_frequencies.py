from collections import Counter
from authorship_attribution._internals.features.base import Feature
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
