from authorship_attribution._internals.features.base import (
    Feature,
    WordsFeatureExtractor,
)
from authorship_attribution._internals.types.aliases import Word


class AverageTypeTokenRatioFeature(Feature):
    def __init__(self, unique_words_count: int, words_count: int) -> None:
        super().__init__()
        self.unique_words_count = unique_words_count
        self.words_count = words_count

    def average_type_token_ratio(self) -> float:
        if self.words_count == 0:
            return 0.0
        return self.unique_words_count / self.words_count


class AverageTypeTokenRatioFeatureExtractor(WordsFeatureExtractor):
    def unique_words_count(self) -> int:
        return len(set[Word](self.words))

    def words_count(self) -> int:
        return len(self.words)

    def feature(self) -> AverageTypeTokenRatioFeature:
        unique_words_count: int = self.unique_words_count()
        words_count: int = self.words_count()
        return AverageTypeTokenRatioFeature(unique_words_count, words_count)
