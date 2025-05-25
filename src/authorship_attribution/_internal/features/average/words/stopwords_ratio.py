from authorship_attribution._internal.features.base.base import Feature


class StopwordsRatioFeature(Feature):
    def __init__(self, stopwords_count: int, total_word_count: int) -> None:
        super().__init__()
        self.stopwords_count = stopwords_count
        self.total_word_count = total_word_count

    def stopwords_ratio(self) -> float:
        if self.total_word_count == 0:
            return 0.0
        return self.stopwords_count / self.total_word_count
