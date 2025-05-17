from typing import Any
from authorship_attribution.__internal._features.base_feature import Feature
from authorship_attribution.__internal._data_types.type_aliases import Json
import json


class PrimitiveFeature(Feature):
    def __init__(self, value: Any):
        super().__init__()
        self.value: Any = value

    def to_json(self) -> Json:
        return json.dumps(self.__dict__, indent=4)

    @staticmethod
    def from_json(json_data: Json) -> "PrimitiveFeature":
        data: dict = json.loads(json_data)
        return PrimitiveFeature(**data)
