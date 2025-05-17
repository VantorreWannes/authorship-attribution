from abc import ABC, abstractmethod
import json
import re

from authorship_attribution._internal.types.aliases import Json


class Feature(ABC):
    @classmethod
    def name(cls) -> str:
        return re.sub(r"(?<!^)(?=[A-Z])", "_", cls.__name__).lower()

    @classmethod
    def file_name(cls) -> str:
        return f"{cls.name()}.json"

    @abstractmethod
    def to_json(self) -> Json:
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, data: Json) -> "Feature":
        pass

    def to_file(self, path: str) -> None:
        json_data = self.to_json()
        with open(path, "w") as file:
            json.dump(json_data, file, indent=4)

    @classmethod
    def from_file(cls, file_path: str) -> "Feature":
        with open(file_path, "r") as file:
            json_data = json.load(file)
            return cls.from_json(json_data)
