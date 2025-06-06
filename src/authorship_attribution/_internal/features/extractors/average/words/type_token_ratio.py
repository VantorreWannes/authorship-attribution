from typing import override

from authorship_attribution._internal.features.average.words.type_token_ratio import (
    TypeTokenRatioFeature,
)
from authorship_attribution._internal.features.extractors.base.words import (
    WordFeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text, Word


class TypeTokenRatioFeatureExtractor(WordFeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__(text)
        self.normalised_words = [word.lower() for word in self.words]

    def unique_words_count(self) -> int:
        unique_words: set[Word] = set[Word](self.normalised_words)
        return len(unique_words)

    def all_words_count(self) -> int:
        return len(self.words)

    @override
    def feature(self) -> TypeTokenRatioFeature:
        unique_words_count = self.unique_words_count()
        all_words_count = self.all_words_count()
        return TypeTokenRatioFeature(unique_words_count, all_words_count)
