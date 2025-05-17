from authorship_attribution._internal.features.base.base import Feature
from authorship_attribution._internal.types.aliases import Json


class ValuesFeature(Feature):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        for key, value in kwargs.items():
            setattr(self, key, value)

    def to_json(self) -> Json:
        return self.__dict__

    @classmethod
    def from_json(cls, data: Json) -> "ValuesFeature":
        return cls(**data)
