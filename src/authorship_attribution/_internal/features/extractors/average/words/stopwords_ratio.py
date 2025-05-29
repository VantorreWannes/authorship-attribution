from typing import override
from nltk.corpus import stopwords

from authorship_attribution._internal.features.extractors.base.words import (
    WordFeatureExtractor,
)
from authorship_attribution._internal.features.average.words.stopwords_ratio import (
    StopwordsRatioFeature,
)
from authorship_attribution._internal.types.aliases import Text

ENGLISH_STOPWORDS = set[str](stopwords.words("english"))


class StopwordsRatioFeatureExtractor(WordFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)

    def stopwords_count(self) -> int:
        count = 0
        for word in self.words:
            if word.lower() in ENGLISH_STOPWORDS:
                count += 1
        return count

    def total_word_count(self) -> int:
        return len(self.words)

    @override
    def feature(self) -> StopwordsRatioFeature:
        sw_count: int = self.stopwords_count()
        total_count: int = self.total_word_count()
        return StopwordsRatioFeature(
            stopwords_count=sw_count, total_word_count=total_count
        )
