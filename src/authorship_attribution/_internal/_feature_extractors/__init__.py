from abc import ABC, abstractmethod
import json
from ._lexical_extractor import (
    AverageWordLengthExtractor,
    AverageWordLengthFeature,
    Average,
)

type Json = str


class Feature(ABC):
    def __init__(self):
        pass

    @abstractmethod
    @staticmethod
    def name() -> str:
        pass

    @abstractmethod
    def _to_json(self) -> Json:
        pass

    @abstractmethod
    @staticmethod
    def _from_json(json_data: Json) -> "Feature":
        pass


class PrimitiveValueFeature(Feature):
    def __init__(self, value: object):
        super().__init__()
        self.value: object = value

    def _to_json(self) -> Json:
        json.dumps(self.__dict__, indent=4)

    @staticmethod
    def _from_json(json_data: Json) -> "PrimitiveValueFeature":
        return json.loads(json_data, object_hook=lambda o: PrimitiveValueFeature(**o))


class FeatureExtractor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def feature(self) -> Feature:
        pass


__all__ = ["Json", "Average", "AverageWordLengthExtractor", "AverageWordLengthFeature"]
