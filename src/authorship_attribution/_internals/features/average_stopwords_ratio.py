from authorship_attribution._internals.features.base import (
    Feature,
    StopwordsFeatureExtractor,
)


class AverageStopwordsRatioFeature(Feature):
    def __init__(self, stopwords_count: int, words_count: int) -> None:
        super().__init__()
        self.stopwords_count = stopwords_count
        self.words_count = words_count

    def average_stopwords_ratio(self) -> float:
        if self.words_count == 0:
            return 0.0
        return self.stopwords_count / self.words_count


class AverageStopwordsRatioFeatureExtractor(StopwordsFeatureExtractor):
    def stopwords_count(self) -> int:
        return len(self.stopwords)

    def words_count(self) -> int:
        return len(self.words)

    def feature(self) -> AverageStopwordsRatioFeature:
        stopwords_count: int = self.stopwords_count()
        words_count: int = self.words_count()
        return AverageStopwordsRatioFeature(stopwords_count, words_count)
