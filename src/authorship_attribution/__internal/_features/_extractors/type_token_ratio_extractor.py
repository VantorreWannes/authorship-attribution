from authorship_attribution.__internal._data_types.type_aliases import Word
from authorship_attribution.__internal._features._extractors.word_extractor import (
    WordFeatureExtractor,
)
from authorship_attribution.__internal._features.type_token_ratio_feature import (
    TypeTokenRatioFeature,
)


class TypeTokenRatioFeatureExtractor(WordFeatureExtractor):
    def _unique_words(self) -> set[Word]:
        return set(self.words)

    def _unique_word_count(self) -> int:
        return len(self._unique_words())

    def _word_count(self) -> int:
        return len(self.words)

    def feature(self) -> TypeTokenRatioFeature:
        return TypeTokenRatioFeature(self._word_count(), self._unique_word_count())
