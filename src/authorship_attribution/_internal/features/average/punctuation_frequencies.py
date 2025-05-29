from authorship_attribution._internal.features.base.base import Feature


class PunctuationFrequenciesFeature(Feature):
    def __init__(
        self, punctuation_counts: dict[str, int], total_punctuation_count: int
    ) -> None:
        super().__init__()
        self.punctuation_counts = punctuation_counts
        self.total_punctuation_count = total_punctuation_count

    def punctuation_frequencies(self) -> dict[str, float]:
        if self.total_punctuation_count == 0:
            return dict[str, float]()
        return {
            char: count / self.total_punctuation_count
            for char, count in self.punctuation_counts.items()
        }
