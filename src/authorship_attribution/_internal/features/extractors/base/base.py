from abc import ABC, abstractmethod
from authorship_attribution._internal.features.base.base import Feature


class FeatureExtractor(ABC):
    @abstractmethod
    def feature(self) -> Feature:
        pass
