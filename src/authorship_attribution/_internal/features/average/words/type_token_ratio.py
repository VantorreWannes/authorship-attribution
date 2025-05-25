from authorship_attribution._internal.features.base.base import Feature


class TypeTokenRatioFeature(Feature):
    def __init__(self, unique_words_count: int, all_words_count: int) -> None:
        super().__init__()
        self.unique_words_count = unique_words_count
        self.all_words_count = all_words_count

    def type_token_ratio(self) -> float:
        return self.unique_words_count / self.all_words_count
