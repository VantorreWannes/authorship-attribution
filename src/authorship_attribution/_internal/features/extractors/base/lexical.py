from authorship_attribution._internal.features.extractors.base.base import (
    FeatureExtractor,
)
from authorship_attribution._internal.types.aliases import Text


class LexicalFeatureExtractor(FeatureExtractor):
    def __init__(self, text: Text) -> None:
        super().__init__()
        self.text: Text = text
