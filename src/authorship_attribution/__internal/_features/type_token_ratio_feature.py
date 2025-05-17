from authorship_attribution.__internal._data_types.type_aliases import Json
from authorship_attribution.__internal._features.base_feature import Feature
import json


class TypeTokenRatioFeature(Feature):
    def __init__(self, word_count: int, unique_word_count: int):
        super().__init__()
        self.word_count = word_count
        self.unique_word_count = unique_word_count

    def type_token_ratio(self) -> float:
        return self.unique_word_count / self.word_count

    def to_json(self) -> Json:
        return json.dumps(self.__dict__, indent=4)

    @staticmethod
    def from_json(json_data: Json) -> "TypeTokenRatioFeature":
        data: dict = json.loads(json_data)
        return TypeTokenRatioFeature(**data)
