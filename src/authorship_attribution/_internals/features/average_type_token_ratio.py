from authorship_attribution._internals.features.base import (
    Feature,
)


class AverageTypeTokenRatioFeature(Feature):
    def __init__(self, unique_words_count: int, words_count: int) -> None:
        super().__init__()
        self.unique_words_count = unique_words_count
        self.words_count = words_count

    def average_type_token_ratio(self) -> float:
        if self.words_count == 0:
            return 0.0
        return self.unique_words_count / self.words_count