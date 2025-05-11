from abc import ABC, abstractmethod
from authorship_attribution.__internal._features.base_feature import Feature


class FeatureExtractor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def feature(self) -> Feature:
        pass
        