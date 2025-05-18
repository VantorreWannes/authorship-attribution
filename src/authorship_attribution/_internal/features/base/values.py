from typing import Any, Generator
from authorship_attribution._internal.features.base.base import Feature
from authorship_attribution._internal.types.aliases import Json


class ValuesFeature(Feature):
    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.__keys = kwargs.keys()
        for key, value in kwargs.items():
            self._set(key, value)

    def _get(self, key: str) -> Any:
        return getattr(self, f"__{key}")

    def _set(self, key: str, value: Any) -> None:
        setattr(self, f"__{key}", value)

    def to_json(self) -> Json:
        return dict[str, Any](self)

    @classmethod
    def from_json(cls, data: Json) -> "ValuesFeature":
        return cls(**data)

    def __iter__(self) -> Generator[tuple[str, Any], Any, None]:
        for key in self.__keys:
            yield key, self._get(key)
