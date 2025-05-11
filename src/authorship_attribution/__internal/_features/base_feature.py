from abc import ABC, abstractmethod
from authorship_attribution.__internal._data_types.type_aliases import Json


class Feature(ABC):
    def __init__(self):
        pass

    @classmethod
    def name(cls: "Feature") -> str:
        return cls.__name__.rstrip("Feature")

    @classmethod
    def file_name(cls: "Feature") -> str:
        return f"{cls.name()}.json"

    @abstractmethod
    def to_json(self) -> Json:
        pass

    @staticmethod
    @abstractmethod
    def from_json(json_data: Json) -> "Feature":
        pass

    def to_file(self, file_path: str) -> None:
        json_data = self.to_json()
        with open(file_path, "w") as file:
            file.write(json_data)

    @classmethod
    def from_file(cls: "Feature", file_path: str) -> "Feature":
        with open(file_path, "r") as file:
            json_data = file.read()
            return cls.from_json(json_data)
