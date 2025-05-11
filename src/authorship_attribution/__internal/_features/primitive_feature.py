from authorship_attribution.__internal._features.base_feature import Feature
from authorship_attribution.__internal._data_types.type_aliases import Json
import json


class PrimitiveFeature(Feature):
    def __init__(self, value: object):
        super().__init__()
        self.value: object = value

    def to_json(self) -> Json:
        return json.dumps(self.__dict__, indent=4)

    @staticmethod
    def from_json(json_data: Json) -> "PrimitiveFeature":
        return json.loads(json_data, object_hook=lambda o: PrimitiveFeature(**o))
