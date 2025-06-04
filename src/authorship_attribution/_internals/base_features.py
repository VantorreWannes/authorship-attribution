from abc import ABC
import json
import re
from typing import Any, Generator

from authorship_attribution._internals.types.aliases import Json


class Feature(ABC):
    @classmethod
    def name(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    @classmethod
    def file_name(cls) -> str:
        return f"{cls.name()}.json"

    def to_json(self) -> Json:
        return dict[str, Any](self)

    @classmethod
    def from_json(cls, data: Json) -> "Feature":
        return cls(**data)

    def to_file(self, path: str) -> None:
        json_data: Json = self.to_json()
        with open(path, "w") as file:
            json.dump(json_data, file, indent=4)

    @classmethod
    def from_file(cls, file_path: str) -> "Feature":
        with open(file_path, "r") as file:
            json_data = json.load(file)
            return cls.from_json(json_data)

    def __iter__(self) -> Generator[tuple[str, Any], Any, None]:
        for key in self.__dict__:
            yield key, getattr(self, key)